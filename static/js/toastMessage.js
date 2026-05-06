document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const messageContainer = document.querySelector('#message-container');
    while(messageContainer.firstChild) {
      messageContainer.removeChild(messageContainer.firstChild);
    }
  }, 5000);
});