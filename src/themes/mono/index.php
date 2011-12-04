<?php
/**
 * 原作者网站: http://www.mono-lab.net/
 * 本人重新制作以用于 Typecho, 并添加一些特效.
 * 
 * @package MonoChrome for Typecho
 * @author Mono-lab & CzBiX
 * @version 1.0.1
 * @link http://czbix.tk
 */
 
  if (!defined('__TYPECHO_ROOT_DIR__')) {
      exit;
  }
  
  $this->need('header.php');
?>

<div id="contents" class="clearfix">
  <div id="left_col">
    <?php $switch_color = 0;
    while($this->next()){
    if ($switch_color==1){ ?>
    <div class="post_even">
    <? } else { ?>
    <div class="post_odd">
    <?php };
	$switch_color = 1 - $switch_color; ?>
      <div class="post clearfix">
        <div class="post_content_wrapper">
          <h2 class="post_title"><a href="<?php $this->permalink(); ?>" rel="bookmark"><?php $this->title(); ?></a></h2>
          <div class="post_content">
            <?php $this->content('Read more'); ?>
          </div>
        </div>
        <dl class="post_meta">
          <dt class="meta_date">
            <?php $this->date('Y'); ?>
          </dt>
          <dd class="post_date">
            <?php $this->date('m'); ?>
            <span>/
            <?php $this->date('d'); ?>
            </span></dd>
          <dt>CATEGORY</dt>
          <dd><?php $this->category(); ?></dd>
          <dt>TAGS</dt>
          <dd><?php $this->tags('<br />', true, 'NONE'); ?></dd>
          <dt class="meta_comment"><a href="<?php $this->permalink(); ?>#comments" title="Comment on <?php $this->title(); ?>"><?php $this->commentsNum('Write comment', '1 Comment', '%d Comments'); ?></a></dt>
        </dl>
      </div>
    </div>
    <?php }; ?>
    <div class="content_noside">
      <div class="page_navi clearfix">
	  	<?php $this->pageNav(); ?>
      </div>
    </div>
  </div>
  <!-- #left_col end -->
  <?php $this->need('sidebar.php'); ?>
</div>
<!-- end #content-->
<?php $this->need('footer.php'); ?>
