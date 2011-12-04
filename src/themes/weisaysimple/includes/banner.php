<?php
//* HEAD
define('HEADER_IMAGE', '%s/images/default.jpg'); // %s is theme dir uri
define('HEADER_IMAGE_WIDTH', 980);
define('HEADER_IMAGE_HEIGHT', 150);
define('NO_HEADER_TEXT', true );
define('HEADER_TEXTCOLOR', 'ffffff'); 
	register_default_headers( array(
		'default' => array(
			'url' => '%s/images/default.jpg',
			'thumbnail_url' => '%s/images/default_img.jpg',
		)
	) );


function admin_header_style() { ?>
<style type="text/css">
#headimg{
	background: url(<?php header_image(); ?>)  no-repeat 0 0;
	color: #333;
	float: left;
	margin: 0;
	padding: 0;
    height: <?php echo HEADER_IMAGE_HEIGHT; ?>px;
    width: <?php echo HEADER_IMAGE_WIDTH; ?>px;
	clear:both;
}
#headimg h1,#desc {
	display: none;
}
.wrap {
	clear:both;
}
#uploadForm  {
	margin:0!important;
}
</style>

<?php }

function header_style() { ?>

<style type="text/css">
.banner img{
	margin: 0 0 5px 0;
}
</style>

<?php }

if ( function_exists('add_custom_image_header') ) {
  add_custom_image_header('header_style', 'admin_header_style');
} 

?>