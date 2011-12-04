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
        <?php $this->archiveTitle(' &raquo; ','',''); ?>
      </ul>
    </div>
    <div class="post clearfix" id="single_post">
      <div class="post_content_wrapper">
        <h2 class="post_title"><span>
          <?php $this->title(); ?>
          </span></h2>
        <div class="post_content">
          <?php $this->content(); ?>
        </div>
        <?php if ($this->options->relatedPost){
        $this->related(5)->to($relatedPosts); ?>
        <?php if ($relatedPosts->have()){ ?>
        <div id="related_post">
          <p class="related_title">Related Post</p>
          <ul>
            <?php while ($relatedPosts->next()){ ?>
            <li><a href="<?php $relatedPosts->permalink(); ?>" title="<?php $relatedPosts->title(); ?>">
              <?php $relatedPosts->title(40,'[...]'); ?>
              </a></li>
            <?php }; ?>
          </ul>
        </div>
        <?php }}; ?>
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
    <div id="comments_wrapper">
      <?php $this->need('comments.php'); ?>
    </div>
  </div>
  <!-- #left_col end -->
  <?php $this->need('sidebar.php'); ?>
</div>
<!-- end #content-->
<?php $this->need('footer.php'); ?>
