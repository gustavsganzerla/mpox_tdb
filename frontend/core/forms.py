from django import forms


class QueryForm(forms.Form):
    sequence_type = forms.ChoiceField(
        label = "Choose a type",
        choices=[('', 'Select an option'),
                 ('cssr', 'CSSR'),
                 ('issr', 'ISSR'),
                 ('ssr', 'SSR'),
                 ('vntr', 'VNTR')],
         widget=forms.Select(attrs={'id':'id_for_sequence_type'}), 
         required=True
        )
    clade = forms.ChoiceField(
            label='Clade',
            choices = [('1', 'Clade 1'), ('2', 'Clade 2')],
            widget = forms.RadioSelect(attrs={'id':'id_for_clade'}), 
            required = False
            )
    
    subclade = forms.ChoiceField(
            label='Subclade',
            choices = [('a', 'a'), ('b', 'b')],
            widget = forms.RadioSelect(attrs={'id':'id_for_subclade'}), 
            required = False
            )
    type = forms.ChoiceField(
        label = "Choose a type",
        choices=[('', 'Select an option'),
                 (1, 'Mono'),
                 (2, 'Di'),
                 (3, 'Tri'),
                 (4, 'Tetra'),
                 (5, 'Penta'),
                 (6, 'Hexa'),
                 ('all', 'All')],
         widget=forms.Select(attrs={'id':'id_for_type'}), 
         required=False
        )
    sequence = forms.CharField(
        required=False,
        label="Genome name",
        widget=forms.TextInput(attrs={'id': 'sequence', 'list':"sequence_list"})
    )

    raw_sequence = forms.CharField(
        required=False,
        label="Raw Genome",
        widget=forms.TextInput(attrs={
            'id': 'raw_sequence',
            'autocomplete': 'off',  
            'placeholder': 'Start typing...'
        })
    )
    
