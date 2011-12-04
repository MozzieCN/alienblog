<?php if (get_option('swt_ada') == 'Display') { ?><div style="display:none"><div id="adsense-loader3" style="display:block;">
<div class="widget"><h3>大家赞助</h3><?php echo stripslashes(get_option('swt_adacode')); ?></div></div></div><?php { echo ''; } ?><?php } else { } ?>
<?php if (get_option('swt_adb') == 'Display') { ?><div style="display:none"><div id="adsense-loader1" style="display:block;float:right;border:1px #ccc solid;padding:2px;margin-left:3px">
<?php echo stripslashes(get_option('swt_adbcode')); ?></div></div><?php { echo ''; } ?><?php } else { } ?>
<?php if (get_option('swt_adc') == 'Display') { ?><div style="display:none"><div id="adsense-loader2" style="display:block; margin-left:20px">
<?php echo stripslashes(get_option('swt_adccode')); ?></div></div><?php { echo ''; } ?><?php } else { } ?>
<div class="clear"></div>
<div id="footer">Copyright <?php echo comicpress_copyright(); ?> <?php bloginfo('name'); ?>. Powered by <a href="http://www.wordpress.org/" rel="external">WordPress</a>.
 Theme by <a href="http://www.weisay.com/" rel="external">Weisay</a>.
 <?php if (get_option('swt_beian') == 'Display') { ?><a href="http://www.miitbeian.gov.cn/" rel="external"><?php echo stripslashes(get_option('swt_beianhao')); ?></a><?php { echo '.'; } ?><?php } else { } ?> <?php if (get_option('swt_tj') == 'Display') { ?><?php echo stripslashes(get_option('swt_tjcode')); ?><?php { echo '.'; } ?>	<?php } else { } ?>
 </div>
<?php wp_footer(); ?>
</div>
</body>
</html>