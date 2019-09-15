/**
 * Test
 */
socket;

ngOnDestroy() {
  this.socket && this.socket.close();
}

initWebsocket() {
  console.log("initWebsocket...")
  // var socket = this.socket = io(document.domain + ':' + location.port + '/test');
  // var socket = this.socket = io(document.domain + ':8890' + '/test',
  var socket = this.socket = io('/test',
    // {
      // secure: true,
      // rejectUnauthorized: false,
    // }
  );

  socket.emit('fetch');

  socket.on('init-data', resp => {
    const data = resp.data || {};

    console.log("on init-data", resp)

  });

  socket.on('status', resp => {
    console.log("on status", resp)
  });
}

onTest(values: any) {
  this._sub03 = this._vulnService.test(this.modelExport)
    .subscribe((resp: any) => {
      console.log("resp", resp)
    });
}
