from django import forms
from root.forms import BaseForm

from .models import Organization, StaticPage


class OrganizationForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "is_featured",
            "sorting_order",
        ]


class StaticPageForm(BaseForm, forms.ModelForm):
    class Meta:
        model = StaticPage
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "slug",
            "sorting_order",
            "is_featured",
        ]


from .models import Branch


class BranchForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Branch
        fields = "__all__"
        exclude = [
            "is_deleted",
            "status",
            "deleted_at",
            "sorting_order",
            "is_featured",
            "organization",
        ]

def check_terminal_in_branch(branch, terminal_no):
    if branch.terminal_set.filter(terminal_no=terminal_no, is_deleted=False).exists():
        return True
    return False

from .models import Terminal

class TerminalForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Terminal
        fields = '__all__'
        exclude = ['is_deleted', 'status', 'deleted_at','sorting_order', 'is_featured']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add a placeholder for the table_number field
        self.fields['terminal_no'].widget.attrs['placeholder'] = 'Enter terminal number'
        self.fields['branch'] = forms.ModelChoiceField(queryset=Branch.objects.filter(is_deleted=False, status=True))

    def clean(self):
        cleaned_data = super().clean()
        terminal_no = cleaned_data.get("terminal_no")
        branch = cleaned_data.get("branch")

        # Only perform validation if this is a creation (no instance provided)
        if not self.instance:
            terminal_exist_flag = check_terminal_in_branch(branch, terminal_no)
    
            if terminal_exist_flag:
                raise forms.ValidationError(f"This terminal {terminal_no} entry already exists in  {branch.name}")            

        return cleaned_data

# def check_table_in_branch(branch, table_no):
#     for terminal in branch.terminal_set.filter(status=True, is_deleted=False):
#         for table in Table.objects.filter(status=True, is_deleted=False, terminal=terminal):
#             if table.table_number==table_no:
#                 return True
#     return False
        

def check_table_in_branch(branch, table_no):
    for terminal in branch.terminal_set.filter(status=True, is_deleted=False):
        for table in Table.objects.filter(status=True, is_deleted=False, terminal=terminal):
            if table.table_number==table_no:
                return True
    return False        


from .models import Table
class TableForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Table
        fields = '__all__'
        exclude = ['is_deleted', 'status', 'deleted_at', "sorting_order",  "is_featured" , 'is_occupied' ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add a placeholder for the table_number field

        self.fields['terminal'] = forms.ModelChoiceField(queryset=Terminal.objects.filter(is_deleted=False, status=True))
        self.fields['table_number'].widget.attrs['placeholder'] = 'Enter table number'
    def clean(self):
        cleaned_data = super().clean()
        terminal = cleaned_data.get("terminal")
        table_number = cleaned_data.get("table_number")
        
        branch= terminal.branch

        table_exist_flag = check_table_in_branch(branch, table_number)

        if table_exist_flag:
            raise forms.ValidationError(f"This table {table_number} entry already exists in  {branch.name}")  

        # Check for duplicate entries
        if Table.objects.filter(terminal=terminal, table_number=table_number).exists():
            print(f"This table {table_number} entry already exists in  {terminal}")
            raise forms.ValidationError(f"This table {table_number} entry already exists in  {terminal}")

        return cleaned_data

from .models import PrinterSetting
class PrinterSettingForm(BaseForm, forms.ModelForm):
    class Meta:
        model = PrinterSetting
        fields = '__all__'
        exclude = ['is_deleted', 'status', 'deleted_at', "sorting_order",  "is_featured" ]
                        

from .models import MailRecipient

class MailRecipientForm(BaseForm, forms.ModelForm):
    class Meta:
        model = MailRecipient
        fields = '__all__'
  