$(function() {
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