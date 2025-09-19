from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, TelField, PasswordField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Email, EqualTo, ValidationError
from app.models.user import User
from app.db import get_db_session

class ReviewForm(FlaskForm):
    """Form for submitting product reviews"""
    user_name = StringField('Tên (tùy chọn)', 
                           validators=[Optional(), Length(max=100)],
                           render_kw={'placeholder': 'Để trống nếu muốn ẩn danh'})
    
    rating = IntegerField('Đánh giá', 
                         validators=[DataRequired(), NumberRange(min=1, max=5, message='Đánh giá từ 1-5 sao')],
                         render_kw={'min': 1, 'max': 5})
    
    content = TextAreaField('Nội dung đánh giá', 
                           validators=[DataRequired(), Length(min=5, message='Nội dung ít nhất 5 ký tự')],
                           render_kw={'rows': 4, 'placeholder': 'Chia sẻ trải nghiệm của bạn về sản phẩm...'})

class CheckoutForm(FlaskForm):
    """Form for checkout process"""
    customer_name = StringField('Họ và tên', 
                               validators=[DataRequired(), Length(max=100)],
                               render_kw={'placeholder': 'Nguyễn Văn A'})
    
    phone = TelField('Số điện thoại', 
                     validators=[DataRequired(), Length(min=10, max=15)],
                     render_kw={'placeholder': '0901234567'})
    
    address = StringField('Địa chỉ', 
                         validators=[DataRequired(), Length(max=200)],
                         render_kw={'placeholder': '123 Đường ABC'})
    
    ward = StringField('Phường/Xã', 
                      validators=[DataRequired(), Length(max=100)],
                      render_kw={'placeholder': 'Phường 1'})
    
    district = StringField('Quận/Huyện', 
                          validators=[DataRequired(), Length(max=100)],
                          render_kw={'placeholder': 'Quận 1'})
    
    province = StringField('Tỉnh/Thành phố', 
                          validators=[DataRequired(), Length(max=100)],
                          render_kw={'placeholder': 'TP.HCM'})
    
    payment_method = SelectField('Phương thức thanh toán',
                                choices=[
                                    ('COD', 'Thanh toán khi nhận hàng (COD)'),
                                    ('MOCK_TRANSFER', 'Chuyển khoản ngân hàng')
                                ],
                                validators=[DataRequired()])


class LoginForm(FlaskForm):
    """Form for user login"""
    email = EmailField('Email', 
                      validators=[DataRequired(), Email()],
                      render_kw={'placeholder': 'example@email.com'})
    
    password = PasswordField('Mật khẩu', 
                            validators=[DataRequired()],
                            render_kw={'placeholder': 'Nhập mật khẩu'})
    
    remember_me = BooleanField('Ghi nhớ đăng nhập')


class RegisterForm(FlaskForm):
    """Form for user registration"""
    username = StringField('Tên đăng nhập', 
                          validators=[DataRequired(), Length(min=3, max=20)],
                          render_kw={'placeholder': 'username'})
    
    email = EmailField('Email', 
                      validators=[DataRequired(), Email()],
                      render_kw={'placeholder': 'example@email.com'})
    
    full_name = StringField('Họ và tên', 
                           validators=[Optional(), Length(max=150)],
                           render_kw={'placeholder': 'Nguyễn Văn A'})
    
    phone = TelField('Số điện thoại', 
                    validators=[Optional(), Length(min=10, max=15)],
                    render_kw={'placeholder': '0901234567'})
    
    password = PasswordField('Mật khẩu', 
                            validators=[DataRequired(), Length(min=6)],
                            render_kw={'placeholder': 'Ít nhất 6 ký tự'})
    
    confirm_password = PasswordField('Xác nhận mật khẩu', 
                                    validators=[DataRequired(), 
                                               EqualTo('password', message='Mật khẩu không khớp')],
                                    render_kw={'placeholder': 'Nhập lại mật khẩu'})
    
    agree_terms = BooleanField('Tôi đồng ý với điều khoản sử dụng', 
                              validators=[DataRequired(message='Bạn phải đồng ý với điều khoản')])
    
    def validate_username(self, username):
        """Check if username already exists"""
        db_session = get_db_session()
        try:
            user = db_session.query(User).filter_by(username=username.data).first()
            if user:
                raise ValidationError('Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.')
        finally:
            db_session.close()
    
    def validate_email(self, email):
        """Check if email already exists"""
        db_session = get_db_session()
        try:
            user = db_session.query(User).filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email đã được đăng ký. Vui lòng sử dụng email khác.')
        finally:
            db_session.close()