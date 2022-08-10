from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo


class CreateShopItemForm(FlaskForm):
    item: StringField('item', validators=[DataRequired()])
    item_url: StringField('item_url', validators=[DataRequired()])
    price: StringField('price', validators=[DataRequired()])

    