var x = document.querySelector('yt-icon[class="style-scope ytd-toggle-button-renderer"]')
if( x != null ) {

  if (x.parentElement.getAttribute('aria-pressed') != 'true'){
  	x.click() ;   
  }
}
