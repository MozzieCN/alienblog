<?php 
if (!defined('__TYPECHO_ROOT_DIR__')) {
    exit;
} ?>
<div id="right_col">
  <div id="information_area" class="clearfix">
    <div class="side_box" id="information">
      <h3>Information</h3>
      <div id="information_contents">
        <?php if ($this->options->monoinfo){
        $this->options->monoinfo();
        } else { ?>
        Welcome to my site,<br />
        Thanks for you visiting!
        <?php }; ?>
      </div>
    </div>
    <div id="entries_rss"> <a href="<?php $this->options->feedUrl(); ?>" title="Entries RSS" >RSS FEED</a> </div>
  </div>
  <div class="side_box" id="search_area_top">
    <div id="search_area" class="clearfix">
      <form method="get" id="searchform" action="http://www.mono-lab.net/demo1/">
        <div>
          <input type="text" name="s" id="search_input" value="Search" onfocus="if(this.value=='Search'){this.value=''; this.style.color = 'white';}" onblur="if(this.value=='')this.value='Search'; this.style.color = 'gray';" />
        </div>
        <div>
          <input type="image" src="<?php $this->options->themeUrl('img/search_button.gif'); ?>" alt="Search from this blog." title="Search from this blog." id="search_button" />
        </div>
      </form>
    </div>
    <div id="tag_list" class="clearfix"> <a href="javascript:void(0);" class="search_tag">TAG LIST</a>
      <ul class='wp-tag-cloud'>
        <?php $this->widget('Widget_Metas_Tag_Cloud','ignoreZeroCount=true&limit=10')->parse('<li><a href="{permalink}" title="{count} topic">{name}</a></li>'); ?>
      </ul>
    </div>
  </div>
  <?php if (empty($this->options->sidebarBlock) || in_array('ShowRecentPosts', $this->options->sidebarBlock)): ?>
  <div class="side_box" id="recent-posts">
    <h3>Recent Posts</h3>
    <ul>
      <?php $this->widget('Widget_Contents_Post_Recent')->parse('<li><a href="{permalink}" title="{commentsNum} Comments">{title}</a></li>'); ?>
    </ul>
  </div>
  <?php endif; ?>
  <?php if (empty($this->options->sidebarBlock) || in_array('ShowRecentComments', $this->options->sidebarBlock)): ?>
  <div class="side_box" id="recent-comments">
    <h3>Recent Comments</h3>
    <ul>
      <?php if (empty($this->options->postBlock) || in_array('relatedPost', $this->options->postBlock)){
        $this->widget('Widget_Comments_Recent','ignoreAuthor=true')->to($comments);
      } else {
        $this->widget('Widget_Comments_Recent')->to($comments);
      } ?>
      <?php while($comments->next()): ?>
      <li>
        <?php $comments->author(true); ?>
        : <a href="<?php $comments->permalink(); ?>" title="Comment at <?php $comments->date('G:i M d'); ?>">
        <?php $comments->excerpt(10, '[...]');?>
        </a></li>
      <?php endwhile; ?>
    </ul>
  </div>
  <?php endif; ?>
  <?php if (empty($this->options->sidebarBlock) || in_array('ShowCategory', $this->options->sidebarBlock)): ?>
  <div class="side_box" id="categorys">
    <h3>Categorys</h3>
    <ul>
      <?php $this->widget('Widget_Metas_Category_List')->parse('<li><a href="{permalink}" title="{count} articles">{name}</a></li>'); ?>
    </ul>
  </div>
  <?php endif; ?>
  <?php if (empty($this->options->sidebarBlock) || in_array('ShowArchive', $this->options->sidebarBlock)): ?>
  <div class="side_box" id="archives">
    <h3>Archives</h3>
    <ul>
      <?php $this->widget('Widget_Contents_Post_Date', 'type=month&format=Y F')->parse('<li><a href="{permalink}" title="{count} articles">{date}</a></li>'); ?>
    </ul>
  </div>
  <?php endif; ?>
  
  <div class="side_box" id="blog-roll">
    <h3>Blog Roll</h3>
    <ul>
    <?php $this->need('links.php'); ?>
    </ul>
  </div>
  
  <?php if (empty($this->options->sidebarBlock) || in_array('ShowOther', $this->options->sidebarBlock)): ?>
  <div class="side_box" id="other">
    <h3>Other</h3>
    <ul>
      <?php if($this->user->hasLogin()): ?>
      <li><a href="<?php $this->options->adminUrl(); ?>">AdminPanel</a></li>
      <li><a href="<?php $this->options->logoutUrl(); ?>">LogOut</a></li>
      <?php else: ?>
      <li class="last"><a href="<?php $this->options->adminUrl('login.php'); ?>">Login</a></li>
      <?php endif; ?>
      <li><a href="http://validator.w3.org/check?uri=referer"><img
        src="http://www.w3.org/Icons/valid-xhtml11-blue.png"
        alt="Valid XHTML 1.1" height="31" width="88" /></a></li>
    </ul>
  </div>
  <?php endif; ?>
</div>
<!-- #right_col end --> 