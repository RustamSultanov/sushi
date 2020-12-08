from babel import Locale
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms import Select, TextInput
from django.forms.widgets import MultiWidget
from django.utils import translation
from phonenumber_field.phonenumber import PhoneNumber

from .models import Messeges, Feedback, Requests, Task, UserProfile, Shop

User = get_user_model()

_COUNTRY_CODE_TO_REGION_CODE = {
    1: (
    "US", "AG", "AI", "AS", "BB", "BM", "BS", "CA", "DM", "DO", "GD", "GU", "JM", "KN", "KY", "LC", "MP", "MS", "PR",
    "SX", "TC", "TT", "VC", "VG", "VI",),
    7: ("RU",),
    20: ("EG",),
    27: ("ZA",),
    30: ("GR",),
    31: ("NL",),
    32: ("BE",),
    33: ("FR",),
    34: ("ES",),
    36: ("HU",),
    39: ("IT", "VA",),
    40: ("RO",),
    41: ("CH",),
    43: ("AT",),
    44: ("GB", "GG", "IM", "JE",),
    45: ("DK",),
    46: ("SE",),
    47: ("NO", "SJ",),
    48: ("PL",),
    49: ("DE",),
    51: ("PE",),
    52: ("MX",),
    53: ("CU",),
    54: ("AR",),
    55: ("BR",),
    56: ("CL",),
    57: ("CO",),
    58: ("VE",),
    60: ("MY",),
    61: ("AU", "CC", "CX",),
    62: ("ID",),
    63: ("PH",),
    64: ("NZ",),
    65: ("SG",),
    66: ("TH",),
    81: ("JP",),
    82: ("KR",),
    84: ("VN",),
    86: ("CN",),
    90: ("TR",),
    91: ("IN",),
    92: ("PK",),
    93: ("AF",),
    94: ("LK",),
    95: ("MM",),
    98: ("IR",),
    211: ("SS",),
    212: ("MA", "EH",),
    213: ("DZ",),
    216: ("TN",),
    218: ("LY",),
    220: ("GM",),
    221: ("SN",),
    222: ("MR",),
    223: ("ML",),
    224: ("GN",),
    225: ("CI",),
    226: ("BF",),
    227: ("NE",),
    228: ("TG",),
    229: ("BJ",),
    230: ("MU",),
    231: ("LR",),
    232: ("SL",),
    233: ("GH",),
    234: ("NG",),
    235: ("TD",),
    236: ("CF",),
    237: ("CM",),
    238: ("CV",),
    239: ("ST",),
    240: ("GQ",),
    241: ("GA",),
    242: ("CG",),
    243: ("CD",),
    244: ("AO",),
    245: ("GW",),
    246: ("IO",),
    247: ("AC",),
    248: ("SC",),
    249: ("SD",),
    250: ("RW",),
    251: ("ET",),
    252: ("SO",),
    253: ("DJ",),
    254: ("KE",),
    255: ("TZ",),
    256: ("UG",),
    257: ("BI",),
    258: ("MZ",),
    260: ("ZM",),
    261: ("MG",),
    262: ("RE", "YT",),
    263: ("ZW",),
    264: ("NA",),
    265: ("MW",),
    266: ("LS",),
    267: ("BW",),
    268: ("SZ",),
    269: ("KM",),
    290: ("SH", "TA",),
    291: ("ER",),
    297: ("AW",),
    298: ("FO",),
    299: ("GL",),
    350: ("GI",),
    351: ("PT",),
    352: ("LU",),
    353: ("IE",),
    354: ("IS",),
    355: ("AL",),
    356: ("MT",),
    357: ("CY",),
    358: ("FI", "AX",),
    359: ("BG",),
    370: ("LT",),
    371: ("LV",),
    372: ("EE",),
    373: ("MD",),
    374: ("AM",),
    375: ("BY",),
    376: ("AD",),
    377: ("MC",),
    378: ("SM",),
    380: ("UA",),
    381: ("RS",),
    382: ("ME",),
    383: ("XK",),
    385: ("HR",),
    386: ("SI",),
    387: ("BA",),
    389: ("MK",),
    420: ("CZ",),
    421: ("SK",),
    423: ("LI",),
    500: ("FK",),
    501: ("BZ",),
    502: ("GT",),
    503: ("SV",),
    504: ("HN",),
    505: ("NI",),
    506: ("CR",),
    507: ("PA",),
    508: ("PM",),
    509: ("HT",),
    590: ("GP", "BL", "MF",),
    591: ("BO",),
    592: ("GY",),
    593: ("EC",),
    594: ("GF",),
    595: ("PY",),
    596: ("MQ",),
    597: ("SR",),
    598: ("UY",),
    599: ("CW", "BQ",),
    670: ("TL",),
    672: ("NF",),
    673: ("BN",),
    674: ("NR",),
    675: ("PG",),
    676: ("TO",),
    677: ("SB",),
    678: ("VU",),
    679: ("FJ",),
    680: ("PW",),
    681: ("WF",),
    682: ("CK",),
    683: ("NU",),
    685: ("WS",),
    686: ("KI",),
    687: ("NC",),
    688: ("TV",),
    689: ("PF",),
    690: ("TK",),
    691: ("FM",),
    692: ("MH",),
    800: ("001",),
    808: ("001",),
    850: ("KP",),
    852: ("HK",),
    853: ("MO",),
    855: ("KH",),
    856: ("LA",),
    870: ("001",),
    878: ("001",),
    880: ("BD",),
    881: ("001",),
    882: ("001",),
    883: ("001",),
    886: ("TW",),
    888: ("001",),
    960: ("MV",),
    961: ("LB",),
    962: ("JO",),
    963: ("SY",),
    964: ("IQ",),
    965: ("KW",),
    966: ("SA",),
    967: ("YE",),
    968: ("OM",),
    970: ("PS",),
    971: ("AE",),
    972: ("IL",),
    973: ("BH",),
    974: ("QA",),
    975: ("BT",),
    976: ("MN",),
    977: ("NP",),
    979: ("001",),
    992: ("TJ",),
    993: ("TM",),
    994: ("AZ",),
    995: ("GE",),
    996: ("KG",),
    998: ("UZ",),
}


class DataAttributesSelect(Select):

    def __init__(self, attrs=None, choices=(), data={}):
        super(DataAttributesSelect, self).__init__(attrs, choices)
        self.data = data

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):  # noqa
        option = super(DataAttributesSelect, self).create_option(name, value, label, selected, index, subindex=None,
                                                                 attrs=None)  # noqa
        # adds the data-attributes to the attrs context var
        for data_attr, values in self.data.items():
            option['attrs'][data_attr] = values[option['value']]

        return option


class PhonePrefixSelect(DataAttributesSelect):
    initial = None

    def __init__(self, initial=None):
        choices = [("", "---------")]
        data = {'data-iso': {'': ''}}
        language = translation.get_language() or settings.LANGUAGE_CODE
        if language:
            locale = Locale(translation.to_locale(language))
            for prefix, values in _COUNTRY_CODE_TO_REGION_CODE.items():
                prefix = "+%d" % prefix
                if initial and initial in values:
                    self.initial = prefix
                for country_code in values:
                    data['data-iso'][prefix] = country_code
                    country_name = locale.territories.get(country_code)
                    if country_name:
                        choices.append((prefix, "{} {}".format(country_name, prefix)))
        super().__init__(choices=sorted(choices, key=lambda item: item[1]),data=data)

    def render(self, name, value, *args, **kwargs):
        return super().render(name, value or self.initial, *args, **kwargs)


class PhoneNumberPrefixWidget(MultiWidget):
    """
    A Widget that splits phone number input into:
    - a country select box for phone prefix
    - an input for local phone number
    """

    def __init__(self, attrs=None, initial=None):
        widgets = (PhonePrefixSelect(initial), TextInput())
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            if type(value) == PhoneNumber:
                if value.country_code and value.national_number:
                    return ["+%d" % value.country_code, value.national_number]
            else:
                return value.split(".")
        return [None, ""]

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        if all(values):
            return "%s.%s" % tuple(values)
        return ""


#     class Meta(RegistrationForm.Meta):
#         model = User
#         fields = [
#             User.USERNAME_FIELD,
#             'first_name',

#         ]
#         widgets = {
#             User.USERNAME_FIELD : PhoneNumberPrefixWidget(attrs={'id':"'data-mask':"(000) 000-00-00"
#         }
#     def __init__(self, *args, **kwargs):
#         super(RegistrationCustomForm, self).__init__(*args, **kwargs)
#         # email_field = User.get_email_field_name()
#         # self.fields[email_field].required = False

#     def save(self,commit=False):
#         user = super(R
# password_check = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Повторите пароль', 'name' : 'password_check'}))

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "form-control"}))


class MessegesForm(forms.ModelForm):
    class Meta:
        model = Messeges
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': "Введите сообщение", 'class': 'form-control'})
        }


class MessegesFileForm(forms.ModelForm):
    class Meta:
        model = Messeges
        fields = ['text', 'file']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': "Введите сообщение", 'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'hidden'})
        }


class StatusTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'btn btn-warning btn-xs btn-round dropdown-toggle'})
        }


class StatusRequestsForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'btn btn-warning btn-xs btn-round dropdown-toggle'})
        }


class StatusFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'btn btn-warning btn-xs btn-round dropdown-toggle'})
        }


class RequestsForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(
                attrs={'name': 'title', 'class': 'form-control', 'placeholder': "Название задачи"}),
            'description': forms.Textarea(
                attrs={'placeholder': "Описание задачи", 'class': "form-control"}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(
                attrs={'name': 'title', 'class': 'form-control', 'placeholder': "Название задачи"}),
            'description': forms.Textarea(
                attrs={'placeholder': "Описание задачи", 'class': "form-control"}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['source', 'description', 'date_pub', 'shop']
        widgets = {
            'source': forms.TextInput(
                attrs={'placeholder': "Источник отзыва", 'class': "form-control"}),
            'description': forms.Textarea(
                attrs={'placeholder': "Текст отзыва", 'class': "form-control", 'rows': '2'}),
            'date_pub': forms.DateInput(
                attrs={'id': "b-m-dtp-date",
                       'class': "form-control",
                       'wtype': 'date',
                       'placeholder': "Выберите дату"}),
            'shop': forms.Select(attrs={'class': "select2 form-control"}),
        }


class RegistrationEmployeeMainForm(forms.ModelForm):
    password_check = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': "Повторите пароль", 'class': 'form-control'}))

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password'
        ]

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': "Почта", 'class': 'form-control', }),
            'first_name': forms.TextInput(attrs={'placeholder': "Имя", 'class': 'form-control', }),
            'username': forms.TextInput(attrs={'placeholder': "Логин", 'class': 'form-control', }),
            'password': forms.PasswordInput(attrs={'placeholder': "Пароль", 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': "Фамилия", 'class': 'form-control', })
        }

    def clean(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже зарегистрирован')
        password_check = self.cleaned_data['password_check']
        password = self.cleaned_data['password']
        if password_check != password:
            raise forms.ValidationError('Пароль не совпадает!')


class RegistrationEmployeeAdditionForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=True
    )

    class Meta:
        model = UserProfile
        exclude = [
            'head', 'manager', 'is_head', 'is_partner', 'is_manager', 'wagtail_profile', 'user', 'ddk_number'
        ]
        widgets = {
            'key_responsibilities': forms.Textarea(
                attrs={'placeholder': "Перечень должностных обязанностей", 'class': "form-control", 'rows': '2'}),
            'phone_number': PhoneNumberPrefixWidget(
                attrs={'data-mask': "(000) 000-00-00", 'class': 'form-control', }),
            'whatsapp': PhoneNumberPrefixWidget(
                attrs={'data-mask': "(000) 000-00-00", 'class': 'form-control', }),
            'twitter': forms.URLInput(attrs={'placeholder': "Twitter", 'class': 'form-control', }),
            'facebook': forms.URLInput(attrs={'placeholder': "Facebook", 'class': 'form-control', }),
            'instagram': forms.URLInput(attrs={'placeholder': "Instagram", 'class': 'form-control', }),
            'middle_name': forms.TextInput(attrs={'placeholder': "Отчество", 'class': 'form-control', }),
            'position': forms.TextInput(attrs={'placeholder': "Должность", 'class': 'form-control', }),

        }


class RegistrationPartnerAdditionForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=True
    )

    class Meta:
        model = UserProfile
        exclude = [
            'head', 'manager', 'is_head', 'is_partner', 'is_manager', 'wagtail_profile',
            'user', 'position', 'key_responsibilities '
        ]
        widgets = {
            # 'key_responsibilities': forms.Textarea(
            #     attrs={'placeholder': "Перечень должностных обязанностей", 'class': "form-control", 'rows': '2'}),
            'phone_number': PhoneNumberPrefixWidget(
                attrs={'data-mask': "(000) 000-00-00", 'class': 'form-control', }),
            'whatsapp': PhoneNumberPrefixWidget(
                attrs={'data-mask': "(000) 000-00-00", 'class': 'form-control', }),
            'twitter': forms.URLInput(attrs={'placeholder': "Twitter", 'class': 'form-control', }),
            'facebook': forms.URLInput(attrs={'placeholder': "Facebook", 'class': 'form-control', }),
            'instagram': forms.URLInput(attrs={'placeholder': "Instagram", 'class': 'form-control', }),
            'middle_name': forms.TextInput(attrs={'placeholder': "Отчество", 'class': 'form-control', }),
            'ddk_number': forms.TextInput(attrs={'placeholder': "Номер ДКК", 'class': 'form-control', }),
            # 'position': forms.TextInput(attrs={'placeholder': "Должность", 'class': 'form-control', }),

        }


class EditEmployeeMainForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email'
        ]

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': "Почта", 'class': 'form-control', }),
            'first_name': forms.TextInput(attrs={'placeholder': "Имя", 'class': 'form-control', }),
            'last_name': forms.TextInput(attrs={'placeholder': "Фамилия", 'class': 'form-control', })
        }


class EditPartnerAdditionForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = [
            'head', 'manager', 'is_head', 'is_partner', 'is_manager', 'wagtail_profile',
            'user', 'position', 'key_responsibilities '
        ]
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(
                attrs={'data-mask': "(000) 000-00-00", 'class': 'form-control', }),
            'whatsapp': PhoneNumberPrefixWidget(
                attrs={'data-mask': "(000) 000-00-00", 'class': 'form-control', }),
            'twitter': forms.URLInput(attrs={'placeholder': "Twitter", 'class': 'form-control', }),
            'facebook': forms.URLInput(attrs={'placeholder': "Facebook", 'class': 'form-control', }),
            'instagram': forms.URLInput(attrs={'placeholder': "Instagram", 'class': 'form-control', }),
            'middle_name': forms.TextInput(attrs={'placeholder': "Отчество", 'class': 'form-control', }),
            'ddk_number': forms.TextInput(attrs={'placeholder': "Номер ДКК", 'class': 'form-control', }),
            'comment': forms.Textarea(attrs={'placeholder': "Коммент", 'class': 'form-control', 'rows': 5}),
        }


class EditEmployeeAdditionForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = [
            'head', 'manager', 'is_head', 'is_partner', 'is_manager', 'wagtail_profile', 'user', 'ddk_number'
        ]
        widgets = {
            'key_responsibilities': forms.Textarea(
                attrs={'placeholder': "Перечень должностных обязанностей", 'class': "form-control", 'rows': '2'}),
            'phone_number': PhoneNumberPrefixWidget(
                attrs={'data-mask': "(000) 000-00-00", 'class': 'form-control', }),
            'whatsapp': PhoneNumberPrefixWidget(
                attrs={'data-mask': "(000) 000-00-00", 'class': 'form-control', }),
            'twitter': forms.URLInput(attrs={'placeholder': "Twitter", 'class': 'form-control', }),
            'facebook': forms.URLInput(attrs={'placeholder': "Facebook", 'class': 'form-control', }),
            'instagram': forms.URLInput(attrs={'placeholder': "Instagram", 'class': 'form-control', }),
            'middle_name': forms.TextInput(attrs={'placeholder': "Отчество", 'class': 'form-control', }),
            'position': forms.TextInput(attrs={'placeholder': "Должность", 'class': 'form-control', }),
        }


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        exclude = [
            'docs', 'checks'
        ]
        widgets = {
            'details': forms.Textarea(attrs={'placeholder': "Реквизиты", 'class': 'form-control', }),
            'address': forms.TextInput(attrs={'placeholder': "Адрес", 'class': 'form-control', }),
            'city': forms.TextInput(attrs={'placeholder': "Город", 'class': 'form-control', }),
            'entity_name': forms.TextInput(attrs={'placeholder': "Юридическое лицо", 'class': 'form-control', }),
            'partner': forms.Select(attrs={'class': "select2 form-control"}),
            'responsibles': forms.SelectMultiple(attrs={'class': 'select2 form-control'}),
            'partner': forms.Select(attrs={'class': "select2 form-control"}),
            'signs': forms.SelectMultiple(attrs={'class': "select2 form-control"}),
        }


class ShopSignEditForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['signs']
        widgets = {'signs': forms.SelectMultiple(attrs={'class': "select2 form-control"})}
