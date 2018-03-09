from django import forms


class CheckInForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    ssn_tail = forms.CharField(label="Last 4 digits of SSN", required=False)


class PatientInfoForm(forms.Form):
    # TODO: Bind dict data to ChoiceFiled Properly
    def __init__(self, *args, **kwargs):
        super(PatientInfoForm, self).__init__(*args, **kwargs)
        # self.fields['gender'] = forms.ChoiceField(choices=args[0]['gender'])
        # self.fields['ethnicity'] = forms.ChoiceField(choices=args[0]['ethnicity'])
        # self.fields['race'] = forms.ChoiceField(choices=args[0]['race'])
    first_name = forms.CharField(max_length=40, required=False)
    middle_name = forms.CharField(max_length=40, required=False)
    last_name = forms.CharField(max_length=40, required=False)
    date_of_birth = forms.DateField(required=True)
    gender = forms.ChoiceField(required=True, choices=(
        ('', 'Select'),
        ('female', 'Female'),
        ('male', 'Male'),
        ('other', 'Other'),
    ))
    city = forms.CharField(max_length=200, required=False)
    zip_code = forms.CharField(max_length=20, required=False)
    state = forms.CharField(max_length=20, required=False)
    home_phone = forms.CharField(required=False)
    cell_phone = forms.CharField(required=False)
    email = forms.CharField(max_length=80, required=False)
    ethnicity = forms.ChoiceField(required=False, choices=(
        ('', 'Select'),
        ('hispanic', 'Hispanic'),
        ('not_hispanic', 'Not Hispanic'),
        ('declined', 'Decline to self-identify'),
    ))
    race = forms.ChoiceField(required=False, choices=(
        ('', 'Select'),
        ('indian', 'Indian'),
        ('asian', 'Asian'),
        ('black', 'Black'),
        ('hawaiian', 'Hawaiian'),
        ('white', 'White'),
        ('declined', 'Decline to self-identify'),
    ))