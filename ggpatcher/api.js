(function(){
  window.ggpatcher = {
    patch: function(patchfile, srcfile){
      var pxhr = new XMLHttpRequest()
      pxhr.open("GET", patchfile, false)
      pxhr.send(null)
      if (pxhr.status == 200){
        sxhr = new XMLHttpRequest()
        sxhr.open("GET", patchfile, false)
        sxhr.send(null)
        if (sxhr.status == 200){
          srcfile = sxhr.responseText.replaceAll('\r', '')
          srcfile = srcfile.split('\n')
          patchfile = JSON.parse(pxhr.responseText)
          patchfile.forEach((patch) => {
            srcfile[patch[0] - 1] = patch[1]
          })
          return srcfile.join('\n')
        }else{
          throw new TypeError(`Failed to load srcfile (got status ${sxhr.status})`)
      }else{
        throw new TypeError(`Failed to load patchfile (got status ${pxhr.status})`)
      }
    },
    load: function(patchfile, srcfile){
      return eval(this.patch(patchfile, srcfile))
    }
  }
})()
