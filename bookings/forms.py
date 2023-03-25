from django import forms

GENDER =(
    ("Boy", "Boy"),
    ("Girl", "Girl"),
)

class GenderForm(forms.Form):
    
    gender = forms.ChoiceField(choices=GENDER, widget=forms.Select(
        attrs={
            'class': 'form-control',
            'name': 'gender',
        }
    ))

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()
        gender = cl_data.get('gender')
        return gender
