<?php 
if (!defined('__TYPECHO_ROOT_DIR__')) {
    exit;
} ?>
  <div id="footer">
   <ul id="copyright">
    <li style="background:none;">
                Copyright &copy;&nbsp; 2011     &nbsp;<a href="<?php $this->options->siteurl(); ?>"><?php $this->options->title(); ?></a> <?php _e('is powered by'); ?> <a href="http://www.typecho.org" rel="external">Typecho)))</a></li>
    <li><a href="http://www.mono-lab.net/" rel="nofollow external">designed by mono-lab</a> , <a href="http://czbix.tk/" rel="external">redesign by CzBiX</a></li>
    <li><a href="<?php $this->options->siteurl('sitemap.xml'); ?>">Sitemap</a></li>
    <li><a href="<?php $this->options->siteurl('About.html'); ?>">About</a></li>
    <li><a id="swtichstyle" href="javascript:void(0);">Switch Style</a></li>
   </ul>
  </div>
 
</div>

<div id="return_top">
 <a href="#wrapper">&nbsp;</a>
</div>
<!-- #footer end -->

<?php $this->footer(); ?>

<!-- #Javascript start -->
<script type="text/javascript" src="http://ajax.aspnetcdn.com/ajax/jquery/jquery-1.4.2.min.js"></script>
<!--script type="text/javascript" src="<?php $this->options->themeUrl('js/jquery.js'); ?>"></script-->
<script type="text/javascript" src="<?php $this->options->themeUrl('js/jscript.js'); ?>"></script>
<!-- #Javascript end -->
</body>
</html>