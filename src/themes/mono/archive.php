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
        <?php $this->archiveTitle('</li><li>','<li>','</li>'); ?>
      </ul>
    </div>
  <?php if ($this->have()){
    $switch_color = 0;
    while($this->next()){
    if ($switch_color==1){ ?>
    <div class="post_even">
    <? } else { ?>
    <div class="post_odd">
    <?php };
	$switch_color = 1 - $switch_color; ?>
      <div class="post clearfix">
        <div class="post_content_wrapper">
          <h2 class="post_title"><a href="<?php $this->permalink(); ?>" rel="bookmark">
            <?php $this->title(); ?>
            </a></h2>
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
          <dd>
            <?php $this->category(); ?>
          </dd>
          <dt>TAGS</dt>
          <dd>
            <?php $this->tags('<br />', true, 'NONE'); ?>
          </dd>
          <dt class="meta_comment"><a href="<?php $this->permalink(); ?>#comments" title="Comment on <?php $this->title(); ?>">
            <?php $this->commentsNum('Write comment', '1 Comment', '%d Comments'); ?>
            </a></dt>
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
  <?php } else { ?>
  <div class="post_odd">
    <div class="post clearfix">
      <div class="post_content_wrapper">
        <h2 class="post_title">
          Not Found
        </h2>
        <div class="post_content">
          Maybe you get lost,<br />
          how about back to <a href="<?php $this->options->siteUrl(); ?>">HOME</a>
        </div>
      </div>
    </div>
  </div>
  <?php }; ?>
  <?php $this->need('sidebar.php'); ?>
</div>
<!-- end #content-->
<?php $this->need('footer.php'); ?>
