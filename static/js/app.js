const BASE_URL = 'http://localhost:5000';
const $messages = $('#messages');
const $html = $('html');
$messages.on('submit', '#messages-form', likes);

async function likes(e) {
  e.preventDefault();
  console.log();
  const resp = await axios.post(`${BASE_URL}/${$(this).attr('action')}`);

  $(this).replaceWith(resp.data.data);
}
