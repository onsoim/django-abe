// Simple Caesar Cipher Encryption
function easy_encryption(input, output) {
    var txt = document.getElementById(input).textContent;
    var res = "";
    for (var i = 0; i < txt.length; i++) {
        if (i%2) res = res.concat('', String.fromCharCode(txt[i].charCodeAt(0) + 1));
        else res = res.concat('', String.fromCharCode(txt[i].charCodeAt(0) - 1));
    }
    document.getElementById(output).value = res;
}

// Simple Caesar Cipher Decryption
function easy_decryption(input, output) {
    var txt = document.getElementById(input).textContent;
    var res = "";
    for (var i = 0; i < txt.length; i++) {
        if (i%2) res = res.concat('', String.fromCharCode(txt[i].charCodeAt(0) - 1));
        else res = res.concat('', String.fromCharCode(txt[i].charCodeAt(0) + 1));
    }
    document.getElementById(output).value = res;
}


var checkAttr = function (attr_user, attr_op, op) {
    // and operation
    if (op) {
        if (attr_user > attr_op) {
            // have all of attributions
            for (var i = 0; 1 << i <= attr_op; i++)
                if (((attr_op >> i) % 2) & !((attr_user >> i) % 2))
                    return 0;
            return 1;
        } else return 0;
    }
    // or operation
    else {
        if (attr_op) {
            // have one of attributions
            for (var i = 0; 1 << i <= attr_op; i++){
                if (((attr_op >> i) % 2) & ((attr_user >> i) % 2))
                    return 1;
            }
            return 0;
        } else return 1;
    }
}
