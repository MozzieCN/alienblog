<?php 
if (!defined('__TYPECHO_ROOT_DIR__')) {
    exit;
}
$this->need('header.php'); ?>

<div id="contents" class="clearfix">
  <div id="left_col">
    <div id="header_meta">
      <ul id="bread_crumb" class="clearfix">
        <li id="bc_home"><a href="<?php $this->options->siteurl(); ?>">HOME</a></li>
        404
      </ul>
    </div>
    <div class="post clearfix" id="single_post">
      <div class="post_content_wrapper">
        <h2 class="post_title"><span>
          404 - File Not Found
          </span></h2>
        <div class="post_content">
          <big>Maybe you get lost,<br />
          how about back to <a href="<?php $this->options->siteUrl(); ?>">HOME</a>
          </big>
        </div>
      </div>
    </div>
  </div>
  <!-- #left_col end -->
  <?php $this->need('sidebar.php'); ?>
</div>
<!-- end #content-->
<?php $this->need('footer.php'); ?>
