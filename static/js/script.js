window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};



// const deleteButton = document.querySelector('#delete');

// deleteButton.onclick= function(e) {
                  
//   let venueId = e.target.dataset.id;
//   console.log(venueId)
//   fetch('/venues/'+venueId+'/delete', {
//       method: 'DELETE',
//       body: null,
//       headers: {
//         "Content-Type": "application/json"
//       }
//   })
//   .then(() => {
//       console.log('Success')
//   })
//   .catch((error) => {
//     console.log(error)
//   })
// }