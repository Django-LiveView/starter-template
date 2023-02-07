// Get lang
export function getLang() {
  return document.querySelector('html').getAttribute("lang");
}

// Prevent body scroll
export function addBodyScrollLock() {
  document.body.classList.add("scroll-lock");
}
export function removeBodyScrollLock() {
    document.body.classList.remove("scroll-lock");
}

export async function encodeFileAsBase64URL(file) {
    if (file) {
	return new Promise((resolve) => {
            const reader = new FileReader();
            reader.addEventListener('loadend', () => {
		resolve(reader.result);
            });
            reader.readAsDataURL(file);
	});
    }
    return null;
}

// The parallax function
export function parallax(el, x, y) {
    if (el) {
    const a = window.innerHeight - el.getBoundingClientRect().top
    el.style.transform = `translate3d(${x * a}px, ${y * a}px, 0)`;
  }
}

// Go to the top page
function scrollToTop () {
    window.scrollTo( {
        top: 0,
        behavior: "smooth",
    });
}

// Renders the HTML received from the Consumer or from indexedDB
export const renderHTML = (data, isBackward = false, isCachingData = false) => {

  const targetHTML = document.querySelector(data.selector);
  if (targetHTML) {
    if (data.append) {
      targetHTML.innerHTML += data.html;
    } else {
        targetHTML.innerHTML = data.html;
    }

    // If it is a new page or is backward, the scroll returns to the beginning
    if ( data.html && !data.scroll && data.url || isBackward ) {
      setTimeout(() => { scrollToTop() }, 50);
    }

  } else {
    console.error(`Target ${data.selector} not found`);
    return;
  }
    // Update URL
    if (data.url) {
	window.history.pushState({ url: data.url }, "", data.url);
    }

    // Update title
    if (data.title) {
	document.title = data.title;
    }
}

export function moveScrollToAnchor(data) {
  if (data.scroll) {
    setTimeout(() => {
      document.querySelector(data.scroll).scrollIntoView({ behavior: "smooth" });
    }, 50)
  }
}
