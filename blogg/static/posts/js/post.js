$(function() {
	// Disable like button if it is already liked by the user
	if (is_post_liked == 'True') {
		$('.like-btn').attr('disabled', 'disabled');
	}
	
	// Disable like button if the post's author is the logged in user.
	if (user.toLowerCase().trim() == post_author.toLowerCase().trim()) {
		$('.like-btn').attr('disabled', 'disabled');
	}
	
	$('.like-btn').click(function() {
		increment_likes(post_id);
	});
});

function increment_likes(post_id) {
	$.get("like/", {post_id: post_id}, function(data){
		$('.likes').html('Likes:' + data);
		$('.like-btn').attr('disabled', 'disabled');
	});
}