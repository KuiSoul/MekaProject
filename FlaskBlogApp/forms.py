from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from FlaskBlogApp.models import User
from flask_login import current_user


def maxImageSize(max_size=2):
    max_bytes = max_size * 1024 * 1024

    def _check_file_size(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(f'Το μέγεθος της εικόνας δεν πρέπει να υπεβαίνει τα {max_size} MB')
    return _check_file_size


def validate_email(form, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError('Αυτό το email υπάρχει ήδη!')


def validate_contact(form, my_contact):
    user = User.query.filter_by(contact_username=my_contact.data).first()
    if my_contact.data != "__init__" and not user:
        raise ValidationError('Ανύπαρκτη επαφή. Ρωτήστε την επαφή σας για το username της.')


class SignupForm(FlaskForm):
    username = StringField( label="Username",
                            validators=[DataRequired( message="Αυτό το πεδίο δε μπορεί να είναι κενό." ),
                                        Length(min=3, max=15,
                                               message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες" )] )
    surname = StringField( label="Surname")
    name = StringField( label="Name",
                            validators=[DataRequired( message="sur name required." ),
                                        Length(min=3, max=15,
                                               message="length error" )] )
    recommender = StringField( label="recommender" )
    email = StringField( label="email",
                         validators=[DataRequired( message="Αυτό το πεδίο δε μπορεί να είναι κενό." ),
                                     Email(message="Παρακαλώ εισάγετε ένα σωστό email"),
                                     validate_email])
    password = StringField( label="password",
                            validators=[DataRequired( message="Αυτό το πεδίο δε μπορεί να είναι κενό." ),
                                        Length(min=3, max=15,
                                               message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες" )] )
    password2 = StringField( label="Επιβεβαίωση password",
                             validators=[DataRequired( message="Αυτό το πεδίο δε μπορεί να είναι κενό." ),
                                         Length(min=3, max=15,
                                                message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες" ),
                                         EqualTo('password',
                                                 message='Τα δύο πεδία password πρέπει να είναι τα ίδια')])
    agree = BooleanField(label="agree", validators=[DataRequired(message='Please check the checkbox')])
    
    submit = SubmitField('Εγγραφή')

    def validate_username(self, username):
        _ = self
        user = User.query.filter_by( username=username.data ).first()
        if user:
            raise ValidationError('Αυτό το username υπάρχει ήδη!' )
    def validate_email_or_username(form, email_username):
        user = User.query.filter(
        (User.username == email_username.data) | (User.email == email_username.data)
    ).first()
        if user:
            raise ValidationError('This username or email already exists.')


class LoginForm(FlaskForm):
    # email_or_username = StringField(label="email or username",
    #                     validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό.")])
    email = StringField(label="email",
                        validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό.")])
    password = StringField( label="password",
                            validators=[DataRequired(message="Αυτό το πεδίο δεν πρέπει να μείνει κενό.")])
    remember_me = BooleanField(label="Remember me")
    submit = SubmitField('Είσοδος')

class ContactForm(FlaskForm):
    option = StringField('Option')
    description = TextAreaField('Description', validators=[DataRequired()])

class NewArticleForm(FlaskForm):
    article_title = StringField(label="Τίτλος Άρθρου",
                                validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                            Length(min=3, max=50,
                                                message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες" )] )

    article_body = TextAreaField( label="Κείμενο Άρθρου",
                                  validators=[DataRequired(message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                              Length(min=5,
                                                     message="Το κείμενο του άρθρου πρέπει να έχει τουλάχιστον 5 "
                                                             "χαρακτήρες" )] )

    article_image = FileField('Εικόνα Άρθρου', validators=[Optional(strip_whitespace=True),
                                                           FileAllowed(['jpg', 'jpeg', 'png'],
                                                                        'Επιτρέπονται μόνο αρχεία εικόνων τύπου jpg, '
                                                                        'jpeg και png!'),
                                                           maxImageSize(max_size=2)])

    submit = SubmitField('Εισαγωγή')


class AccountUpdateForm(FlaskForm):
    username = StringField( label="Username",
                            validators=[DataRequired( message="Αυτό το πεδίο δε μπορεί να είναι κενό." ),
                                        Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 "
                                                                       "χαρακτήρες")])
    email = StringField( label="email",
                         validators=[DataRequired( message="Αυτό το πεδίο δε μπορεί να είναι κενό."),
                                     Email(message="Παρακαλώ εισάγετε ένα σωστό email")])

    profile_image = FileField('Εικόνα Προφίλ',
                              validators=[Optional( strip_whitespace=True ),
                                          FileAllowed( ['jpg', 'jpeg', 'png'],
                                                       'Επιτρέπονται μόνο αρχεία εικόνων τύπου jpg, jpeg και png!' ),
                                          maxImageSize(max_size=2)])
    submit = SubmitField('Τροποποίηση')

    def validate_username(self, username):
        _ = self
        if username.data != current_user.username:
            user = User.query.filter_by( username=username.data ).first()
            if user:
                raise ValidationError( 'Αυτό το username υπάρχει ήδη!' )

    def validate_email(self, email):
        _ = self
        if email.data != current_user.email:
            user = User.query.filter_by( email=email.data ).first()
            if user:
                raise ValidationError('Αυτό το email υπάρχει ήδη!')


class NewOfferForm(FlaskForm):

    offer_title = StringField(label="Θέμα",
                              validators=[DataRequired(message="Αυτό το πεδίο δεν πρέπει να είναι κενό."),
                                          Length(min=3, max=50, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 "
                                                                          "χαρακτήρες.")])
    offer_type = StringField(label="Είδος Διαφήμισης",
                              validators=[DataRequired(message="Αυτό το πεδίο δεν πρέπει να είναι κενό."),
                                          Length(min=3, max=50, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 "
                                                                          "χαρακτήρες.")])
    offer_location = StringField(label="Τοποθεσία",
                              validators=[DataRequired(message="Αυτό το πεδίο δεν πρέπει να είναι κενό."),
                                          Length(min=3, max=50, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 "
                                                                          "χαρακτήρες.")])
    offer_body = TextAreaField( label="Κείμενο",
                                validators=[DataRequired(message="Αυτό το πεδίο δεν πρέπει να είναι κενό."),
                                            Length(min=50, message="Το κείμενο του άρθρου πρέπει να έχει τουλάχιστον "
                                                                   "50 χαρακτήρες.")])
    offer_image = FileField('Εικόνα προσφοράς', validators=[Optional(strip_whitespace=True),
                                                            FileAllowed(['jpg', 'jpeg', 'png'],
                                                                            'Επιτρέπονται μόνο αρχεία εικόνων τύπου jpg, '
                                                                            'jpeg και png!'),
                                                            maxImageSize(max_size=2)])

    submit = SubmitField('Καταχώριση')
