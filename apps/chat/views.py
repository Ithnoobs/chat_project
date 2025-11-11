from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Room, Message, RoomMembership
from .forms import RoomCreateForm

@login_required
def room_list(request):
    # Get rooms the user is a member of with member count
    user_rooms = Room.objects.filter(members=request.user).prefetch_related('members__profile').order_by('-created_at')
    
    # Get public rooms
    public_rooms = Room.objects.filter(room_type='public').exclude(members=request.user).prefetch_related('members')[:10]
    
    # Get online members count for each room
    for room in user_rooms:
        room.online_count = room.members.filter(profile__online_status='online').count()
    
    context = {
        'user_rooms': user_rooms,
        'public_rooms': public_rooms,
    }
    return render(request, 'chat/room_list.html', context)

@login_required
def room_detail(request, slug):
    room = get_object_or_404(Room, slug=slug)
    
    # Check if user is a member or if room is public
    is_member = RoomMembership.objects.filter(user=request.user, room=room).exists()
    
    if not is_member:
        if room.room_type == 'public':
            # Auto-join public rooms
            RoomMembership.objects.create(user=request.user, room=room, role='member')
            messages.success(request, f'You joined {room.name}!')
        else:
            messages.error(request, 'You do not have access to this private room.')
            return redirect('chat:room_list')
    
    # Get messages
    messages_list = room.messages.filter(is_deleted=False).select_related('sender', 'sender__profile')[:50]
    
    # Get members
    members = room.members.all()
    
    context = {
        'room': room,
        'messages': messages_list,
        'members': members,
    }
    return render(request, 'chat/room_detail.html', context)

@login_required
def room_create(request):
    if request.method == 'POST':
        form = RoomCreateForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.created_by = request.user
            room.save()
            
            # Add creator as admin member
            RoomMembership.objects.create(user=request.user, room=room, role='admin')
            
            messages.success(request, f'Room "{room.name}" created successfully!')
            return redirect('chat:room_detail', slug=room.slug)
    else:
        form = RoomCreateForm()
    
    return render(request, 'chat/room_create.html', {'form': form})