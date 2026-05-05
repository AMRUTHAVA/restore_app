/**
=========================================================================
=========================================================================
Template Name: Mantis - Admin Template
Author: CodedThemes
Support: https://codedthemes.support-hub.io/
File: themes.js
Description:  this file will contains overall theme setup and handle
              behavior of live custumizer like Dark/Light, LTR/RTL,
              preset color, theme layout, theme contarast etc.
=========================================================================
=========================================================================
*/

var rtl_flag = false;
var dark_flag = false;

function layout_change_default() {
  // Determine the initial layout based on the user's system preference for color scheme
  const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
  let dark_layout = prefersDarkScheme.matches ? 'dark' : 'light';

  // Apply the initial layout
  layout_change(dark_layout);

  // Set the active class on the default theme button, if it exists
  const btn_control = document.querySelector('.theme-layout .btn[data-value="default"]');
  if (btn_control) {
    btn_control.classList.add('active');
  }

  // Listen for changes in the user's system color scheme preference
  prefersDarkScheme.addEventListener('change', (event) => {
    dark_layout = event.matches ? 'dark' : 'light';
    layout_change(dark_layout);
  });
}

// dark switch mode
function dark_mode() {
  const darkModeToggle = document.getElementById('dark-mode');

  // Ensure the element exists before proceeding
  if (!darkModeToggle) return;

  // Toggle between dark and light modes based on the checkbox status
  const mode = darkModeToggle.checked ? 'dark' : 'light';
  layout_change(mode);
}

// preset color
document.addEventListener('DOMContentLoaded', function () {
  // Handle preset color changes
  const presetColors = document.querySelectorAll('.preset-color > a');
  if (presetColors.length) {
    presetColors.forEach((colorElement) => {
      colorElement.addEventListener('click', function (event) {
        let targetElement = event.target;

        // Traverse up to find the correct clickable element
        if (targetElement.tagName === 'SPAN') {
          targetElement = targetElement.parentNode;
        } else if (targetElement.tagName === 'IMG') {
          targetElement = targetElement.closest('a');
        }

        const presetValue = targetElement.getAttribute('data-value');
        preset_change(presetValue);
      });
    });
  }

  // Initialize SimpleBar if .pct-body exists
  const pctBody = document.querySelector('.pct-body');
  if (pctBody) {
    new SimpleBar(pctBody);
  }

  // Handle layout reset
  const layoutResetBtn = document.querySelector('#layoutreset');
  if (layoutResetBtn) {
    layoutResetBtn.addEventListener('click', () => location.reload());
  }

  // Handle RTL layout toggle
  const rtlLayoutToggle = document.querySelector('#layoutmodertl');
  if (rtlLayoutToggle) {
    rtlLayoutToggle.addEventListener('click', () => {
      const isChecked = rtlLayoutToggle.checked ? 'true' : 'false';
      layout_rtl_change(isChecked);
    });
  }
});

// funcation for Manage the font in the preset UI
function font_change(name) {
  let fontMap = {
    Roboto: 'https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap',
    Poppins: 'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap',
    Inter: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap',
    'Public Sans': 'https://fonts.googleapis.com/css2?family=Public+Sans:wght@300;400;500;600;700&display=swap'
  };

  // Normalize the font name if needed
  name = name === 'Public-Sans' ? 'Public Sans' : name;

  // Get the font source URL
  const src = fontMap[name];
  if (src) {
    // Update the font link
    document.querySelector('#main-font-link').setAttribute('href', src);

    // Set the font-family on body
    document.body.style.fontFamily = `"${name}", sans-serif`;

    // Manage the active state in the font preset UI
    const control = document.querySelector('.pct-offcanvas');
    if (control) {
      if (document.querySelector('.fontpreset-color > a.active')) {
        document.querySelector('.fontpreset-color > a.active').classList.remove('active');
      }
      document.querySelector(`.fontpreset-color > a[data-value='${name}']`).classList.add('active');
    }
  }
}

function preset_change(value) {
  const body = document.querySelector('body');
  const control = document.querySelector('.pct-offcanvas');

  // Set the 'data-pc-preset' attribute on the body
  body.setAttribute('data-pc-preset', value);

  // Update active state in the UI if control exists
  if (control) {
    const activeElement = document.querySelector('.preset-color > a.active');
    const newActiveElement = document.querySelector(`.preset-color > a[data-value='${value}']`);

    if (activeElement) {
      activeElement.classList.remove('active');
    }
    if (newActiveElement) {
      newActiveElement.classList.add('active');
    }
  }
}

function layout_rtl_change(value) {
  const body = document.querySelector('body');
  const html = document.querySelector('html');
  const directionControl = document.querySelector('.theme-direction .btn.active');
  const rtlBtn = document.querySelector(".theme-direction .btn[data-value='true']");
  const ltrBtn = document.querySelector(".theme-direction .btn[data-value='false']");

  if (value === 'true') {
    rtl_flag = true;
    body.setAttribute('data-pc-direction', 'rtl');
    html.setAttribute('dir', 'rtl');
    html.setAttribute('lang', 'ar');

    // Update active button state for RTL
    if (directionControl) directionControl.classList.remove('active');
    if (rtlBtn) rtlBtn.classList.add('active');
  } else {
    rtl_flag = false;
    body.setAttribute('data-pc-direction', 'ltr');
    html.removeAttribute('dir');
    html.removeAttribute('lang');

    // Update active button state for LTR
    if (directionControl) directionControl.classList.remove('active');
    if (ltrBtn) ltrBtn.classList.add('active');
  }
}

// =================================================
function layout_change(layout) {
  const body = document.querySelector('body');
  const pctOffCanvas = document.querySelector('.pct-offcanvas');
  const defaultBtnControl = document.querySelector('.theme-layout > a[data-value="default"]');
  const activeBtnControl = document.querySelector('.theme-layout > a.active');

  body.setAttribute('data-pc-theme', layout);

  if (defaultBtnControl) {
    defaultBtnControl.classList.remove('active');
  }

  // Helper function to set logo sources based on theme
  function setLogoSources(theme) {
    const logoSources = {
      dark: '../assets/images/logo-white.svg',
      light: '../assets/images/logo-dark.svg'
    };
    const logoSrc = theme === 'dark' ? logoSources.dark : logoSources.light;

    const sidebarLogo = document.querySelector('.pc-sidebar .m-header .logo-lg');
    const navbarLogo = document.querySelector('.navbar-brand .logo-lg');
    const authFooterLogo = document.querySelector('.auth-main.v1 .auth-sidefooter img');
    const footerLogo = document.querySelector('.footer-top .footer-logo');

    if (sidebarLogo) sidebarLogo.setAttribute('src', logoSrc);
    if (navbarLogo) navbarLogo.setAttribute('src', logoSrc);
    if (authFooterLogo) authFooterLogo.setAttribute('src', logoSrc);
    if (footerLogo) footerLogo.setAttribute('src', logoSrc);
  }

  // Apply theme-specific settings
  if (layout === 'dark') {
    dark_flag = true;
    setLogoSources('dark');

    if (activeBtnControl) {
      activeBtnControl.classList.remove('active');
      document.querySelector(".theme-layout > a[data-value='true']").classList.add('active');
    }
  } else {
    dark_flag = false;
    setLogoSources('light');

    if (activeBtnControl) {
      activeBtnControl.classList.remove('active');
      document.querySelector(".theme-layout > a[data-value='false']").classList.add('active');
    }
  }
}

function change_box_container(value) {
  const content = document.querySelector('.pc-content');
  const footerWrapper = document.querySelector('.footer-wrapper');
  const activeControl = document.querySelector('.theme-container > a.active');

  // Check if content and footer elements exist
  if (content && footerWrapper) {
    const isBoxed = value === 'true';

    // Helper function to toggle class names
    function toggleContainer(isBoxed) {
      if (isBoxed) {
        content.classList.add('container');
        footerWrapper.classList.add('container');
        footerWrapper.classList.remove('container-fluid');
      } else {
        content.classList.remove('container');
        footerWrapper.classList.remove('container');
        footerWrapper.classList.add('container-fluid');
      }
    }

    toggleContainer(isBoxed);

    // Update active button class
    if (activeControl) {
      activeControl.classList.remove('active');
      const newActive = document.querySelector(`.theme-container > a[data-value='${value}']`);
      if (newActive) {
        newActive.classList.add('active');
      }
    }
  }
}
