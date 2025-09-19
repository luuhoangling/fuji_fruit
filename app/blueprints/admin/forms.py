from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, BooleanField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, ValidationError
from wtforms.widgets import TextArea

class ProductForm(FlaskForm):
    """Form for creating/editing products"""
    name = StringField('Tên sản phẩm', 
                      validators=[DataRequired(), Length(max=200)],
                      render_kw={'placeholder': 'Nhập tên sản phẩm'})
    
    slug = StringField('Slug', 
                      validators=[DataRequired(), Length(max=200)],
                      render_kw={'placeholder': 'ten-san-pham'})
    
    short_desc = TextAreaField('Mô tả ngắn', 
                              validators=[Optional(), Length(max=500)],
                              render_kw={'rows': 3, 'placeholder': 'Mô tả ngắn về sản phẩm'})
    
    image_url = StringField('URL hình ảnh', 
                           validators=[Optional(), Length(max=500)],
                           render_kw={'placeholder': 'https://example.com/image.jpg'})
    
    price = DecimalField('Giá gốc', 
                        validators=[DataRequired(), NumberRange(min=0, message='Giá phải lớn hơn 0')],
                        render_kw={'step': '1000', 'placeholder': '100000'})
    
    is_active = BooleanField('Kích hoạt', default=True)
    
    # Sale pricing fields
    sale_price = DecimalField('Giá khuyến mãi', 
                             validators=[Optional(), NumberRange(min=0)],
                             render_kw={'step': '1000', 'placeholder': '80000'})
    
    sale_start = DateField('Ngày bắt đầu KM', 
                          validators=[Optional()],
                          render_kw={'type': 'date'})
    
    sale_end = DateField('Ngày kết thúc KM', 
                        validators=[Optional()],
                        render_kw={'type': 'date'})
    
    def validate_sale_price(self, field):
        if field.data and self.price.data and field.data >= self.price.data:
            raise ValidationError('Giá khuyến mãi phải nhỏ hơn giá gốc')
    
    def validate_sale_end(self, field):
        if field.data and self.sale_start.data and field.data <= self.sale_start.data:
            raise ValidationError('Ngày kết thúc phải sau ngày bắt đầu')

class StockForm(FlaskForm):
    """Form for managing product stock"""
    qty_on_hand = IntegerField('Số lượng tồn kho', 
                               validators=[DataRequired(), NumberRange(min=0, message='Số lượng không được âm')],
                               render_kw={'placeholder': '100'})

class CategoryForm(FlaskForm):
    """Form for creating/editing categories"""
    name = StringField('Tên danh mục', 
                      validators=[DataRequired(), Length(max=100)],
                      render_kw={'placeholder': 'Nhập tên danh mục'})
    
    slug = StringField('Slug', 
                      validators=[DataRequired(), Length(max=100)],
                      render_kw={'placeholder': 'ten-danh-muc'})
    
    parent_id = SelectField('Danh mục cha', 
                           coerce=int,
                           validators=[Optional()],
                           choices=[])  # Will be populated in the view

class OrderStatusForm(FlaskForm):
    """Form for updating order status"""
    status = SelectField('Trạng thái đơn hàng',
                        choices=[
                            ('pending', 'Chờ xác nhận'),
                            ('confirmed', 'Đã xác nhận'),
                            ('fulfilled', 'Đã giao hàng'),
                            ('cancelled', 'Đã hủy')
                        ],
                        validators=[DataRequired()])