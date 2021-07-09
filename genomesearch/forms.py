from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired

import email_validator


class RegistrationForm(FlaskForm):
    username = StringField('Username',  validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[
                                    DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class TestForm(FlaskForm):
    submit = SubmitField('ClickButton')

class SortForm(FlaskForm):
    sortSNIPId = BooleanField('SNIP ID')
    sortName = BooleanField('Name')
    sortCm = BooleanField('cM')
    sortChromosome = BooleanField('Chromosome')

class SearchForm(FlaskForm):
    genomeName = StringField('SNP ID', [validators.Length(min=0, max=25)])
    genomeChrom = StringField('Chromosome', [validators.Length(min=0, max=25)])
    genomeCultivar = StringField('Cultivar', [validators.Length(min=0, max=50)])
    lowerCM = DecimalField('Lower', [validators.Optional(strip_whitespace=True)])
    upperCM = DecimalField('Upper', [validators.Optional(strip_whitespace=True)])
    #genomeRange = StringField('GenomeRange', validators=[])
    chrom1A = BooleanField('1A')
    chrom1B = BooleanField('1B')
    chrom1D = BooleanField('1D')
    
    chrom2A = BooleanField('2A')
    chrom2B = BooleanField('2B')
    chrom2D = BooleanField('2D')

    chrom3A = BooleanField('3A')
    chrom3B = BooleanField('3B')
    chrom3D = BooleanField('3D')

    chrom4A = BooleanField('4A')
    chrom4B = BooleanField('4B')
    chrom4D = BooleanField('4D')

    chrom5A = BooleanField('5A')
    chrom5B = BooleanField('5B')
    chrom5D = BooleanField('5D')

    chrom6A = BooleanField('6A')
    chrom6B = BooleanField('6B')
    chrom6D = BooleanField('6D')

    chrom7A = BooleanField('7A')
    chrom7B = BooleanField('7B')
    chrom7D = BooleanField('7D')

    submit = SubmitField('Search Database')
