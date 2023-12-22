export default function get_lists<T>(type: string, service: any): Promise<T[]> {
  return new Promise((resolve, reject) => {
    let list;
    let call;

    switch (type) {
      case 'Users':
        call = service.getUsers();
        break;
      case 'Rooms':
        call = service.getRooms();
        break;
      case 'Bookings':
          call = service.getBookings();
          break;
      case 'Reviews':
        call = service.getReviews();
        break;
      default:
        reject(`Type ${type} not recognized`);
        return; 
    }

    call.then((temp_list: any) => {
      list = temp_list;
      resolve(list);
    }).catch((error: any) => {
      reject(error);
    });
  });
}


// Chat-GPT CODE:

// export default function get_lists<T>(type: string, service: any): Promise<T[]> {
//   return new Promise((resolve, reject) => {
//     let list;

//     switch (type) {
//       case 'Users':
//         service.getUsers().then((user_list: any) => {
//           list = user_list;
//           resolve(list);
//         }).catch((error: any) => {
//           reject(error);
//         });
//         break;
//       case 'Rooms':
//         service.GetRooms().then((room_list: any) => {
//           list = room_list;
//           resolve(list);
//         }).catch((error: any) => {
//           reject(error);
//         });
//         break;
//       case 'Reviews':
//         service.getReviews().then((review_list: any) => {
//           list = review_list;
//           resolve(list);
//         }).catch((error: any) => {
//           reject(error);
//         });
//         break;
//       default:
//         reject(`Type ${type} not recognized`);
//         break;
//     }
//   });
// }
