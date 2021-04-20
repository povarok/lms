from django.shortcuts import render, get_object_or_404, redirect
from .serializers import UserTestGroupSerializer, ControlTestSerializer
from .models import *
import json

def control_page(request):
    group_constructors = TestGroupConstructor.objects.all()
    groups = []
    for constructor in group_constructors:
        group, _ = UserTestGroup.objects.get_or_create(user=request.user, constructor=constructor)
        groups.append(group)
    serializer = UserTestGroupSerializer(groups, many=True, read_only=True)
    groups = serializer.data
    print(len(groups))
    for group in groups:
        for test in group['constructor']['tests']:
            test['control_tests'] = ControlTestSerializer(ControlTest.objects.filter(user=request.user, apparatus=test['id']), many=True, read_only=True).data
        group['active'] = True
        if groups.index(group) > 0:
            print(groups.index(group))
            if not groups[groups.index(group) - 1]['is_complete']:
                group['active'] = False
    context = {
        "groups": json.loads(json.dumps(groups))
    }
    return render(request, "mysite/control.html", context)