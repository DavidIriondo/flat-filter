from wtforms import BooleanField, IntegerField, StringField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm

class FilterForm(FlaskForm):
    class Meta:
        csrf = False

    province = StringField('Provincia', validators=[DataRequired()])
    municipality = StringField('Municipio', validators=[DataRequired()])
    min_price = IntegerField('Precio minimo', render_kw={"step": "50"}, validators=[NumberRange(min=100, message="El precio mínimo no puede ser menor que 0")])
    max_price = IntegerField('Precio maximo',  render_kw={"step": "50"})
    room_numbers = SelectField(u'Nº habitaciones', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')],)

    def __str__(self):
        return (f"FilterForm(province={self.province.data!r}, "
                f"municipality={self.municipality.data!r}, "
                f"min_price={self.min_price.data}, "
                f"max_price={self.max_price.data}, "
                f"room_numbers={self.room_numbers.data})")