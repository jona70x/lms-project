from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import Course, Announcement
from app.config import db
from app.announcements import announcements_bp
from app.announcements.announcement_form import AnnouncementForm
from app.decorators import roles_required
from app.models import User


# Create new announcement
@announcements_bp.route('/new', methods=['GET', 'POST'])
@announcements_bp.route('/new/<int:course_id>', methods=['GET', 'POST'])
@login_required
@roles_required(User.ROLE_PROFESSOR, User.ROLE_ADMIN)
def create_announcement(course_id=None):
    form = AnnouncementForm()
    course = None
    
    # Get course if course_id is provided
    if course_id:
        course = Course.query.get_or_404(course_id)
        form.course_id.data = course_id

    if form.validate_on_submit():
        # Use course_id from URL if provided, otherwise from form
        final_course_id = course_id if course_id else form.course_id.data
        
        announcement_data = {
            'course_id': final_course_id,
            'title': form.title.data,
            'content': form.content.data
        }

        new_announcement = Announcement(**announcement_data)

        db.session.add(new_announcement)
        db.session.commit()

        flash('Announcement created!', 'success')
        
        # back to dashboard
        if course_id:
            return redirect(url_for('courses.course_dashboard', course_id=course_id, tab='announcements'))

        return redirect(url_for('courses.courses_list'))
    
    return render_template('announcements/new_announcement.html', form=form, course_id=course_id, course=course)


# Update announcement
@announcements_bp.route('/<int:announcement_id>/update', methods=['GET', 'POST'])
@login_required
@roles_required(User.ROLE_PROFESSOR, User.ROLE_ADMIN)
def update_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    course = announcement.course
    form = AnnouncementForm()

    # Pre-populate form on GET request
    if request.method == 'GET':
        form.course_id.data = course.id
        form.title.data = announcement.title
        form.content.data = announcement.content
    
    # Updating all fields
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.content = form.content.data
        db.session.commit()

        flash('Announcement updated!', 'success')
        return redirect(url_for('courses.course_dashboard', course_id=announcement.course_id, tab='announcements'))

    return render_template('announcements/update_announcement.html', form=form, announcement=announcement, course=course)


# Delete announcement
@announcements_bp.route('/<int:announcement_id>/delete', methods=['POST'])
@login_required
@roles_required(User.ROLE_PROFESSOR, User.ROLE_ADMIN)
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    course_id = announcement.course_id
    
    db.session.delete(announcement)
    db.session.commit()
    
    flash('Announcement deleted!', 'success')
    return redirect(url_for('courses.course_dashboard', course_id=course_id, tab='announcements'))
