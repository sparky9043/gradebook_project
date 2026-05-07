document.addEventListener('DOMContentLoaded', () => {
  // Show Dialog Button
  const showStudentDialogBtn = document.querySelector('#show-student-dialog-btn');

  // Close Dialog Buttons
  const closeStudentDialogBtn = document.querySelector('#close-student-dialog-btn');
  const cancelAddStudentBtn = document.querySelector('#cancel-add-student-btn');

  // Dialog Element
  const addStudentDialog = document.querySelector('dialog#add-student-dialog');
  

  // Event Listener on Show Dialog Button
  if (addStudentDialog) {
    showStudentDialogBtn.addEventListener('click', () => {
      addStudentDialog.showModal();
    });
    // Event Listener on both Close Dialog Buttons
    const cancelButtons = [closeStudentDialogBtn, cancelAddStudentBtn];
  
    cancelButtons.forEach((button) => button.addEventListener('click', () => {
      addStudentDialog.close();
    }));
  }
  

});