from django.contrib import admin

from general.models import (
    Persone, PCAPFile, CSVFile,
    Group, Trafic, Interface,
    Package, Trafic
)


admin.site.register(Persone)
admin.site.register(PCAPFile)
admin.site.register(CSVFile)
admin.site.register(Group)
admin.site.register(Trafic)
admin.site.register(Interface)
admin.site.register(Package)
