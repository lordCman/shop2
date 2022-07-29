from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from app.ig.forms import PostForm
from app.models import Post, db


ig = Blueprint('ig', __name__, template_folder='igtemplates')


@ig.route('/posts/create', methods=["GET","POST"])
@login_required
def createPost():
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post = Post(title, img_url, caption, current_user.id)
            post.save()
            flash('Successfully created post.', 'success')
        else:
            flash('Invalid form. Please fill out the form correctly.', 'danger')
    return render_template('createpost.html', form=form)

@ig.route('/posts')
def getAllPosts():
    posts = Post.query.all()
    return render_template('feed.html', posts=posts)


@ig.route('/posts/<int:post_id>')
def getSinglePost(post_id):
    post = Post.query.get(post_id)
    # post = Post.query.filter_by(id=post_id).first()
    return render_template('singlepost.html', post=post)

@ig.route('/posts/update/<int:post_id>', methods=["GET", "POST"])
def updatePost(post_id):
    form = PostForm()
    # post = Post.query.get(post_id)
    post = Post.query.filter_by(id=post_id).first()
    if current_user.id != post.user_id:
        flash('You are not allowed to update another user\'s posts.', 'danger')
        return redirect(url_for('ig.getSinglePost', post_id=post_id))
    if request.method=="POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post.updatePostInfo(title,img_url,caption)
            post.saveUpdates()
            flash('Successfully updated post.', 'success')
            return redirect(url_for('ig.getSinglePost', post_id=post_id))
        else:
            flash('Invalid form. Please fill out the form correctly.', 'danger')
    return render_template('updatepost.html', form=form,  post=post)


@ig.route('/posts/delete/<int:post_id>')
def deletePost(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        flash('You are not allowed to delete another user\'s posts.', 'danger')
        return redirect(url_for('ig.getSinglePost', post_id=post_id))
    post.delete()
    flash('Successfully delete post.', 'success')
    return redirect(url_for('ig.getAllPosts'))