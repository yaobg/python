let vm = new Vue({
    el: "#app",
//                delimiters:['[[","]]'],
    delimiters: ['[[', ']]'],
    data: {
        //                    v-model
        username: "",
        password: "",
        password2: "",
        mobile: "",
        allow: "",
        uuid: "",
        img_db: "",
        img_code_url: "",
        code_message: "　验证码",
        msg: "",
        inte: "",


        //                    error_message
        error_name_message: "",
        error_pass_message: "",
        error_phone_massage: "",
        error_img_message: "",
        error_message_msg: "",
        ssm_code_message: "发送",


        //                    v-show
        error_name: false,
        error_pass: false,
        error_pass2: false,
        error_phone: false,
        error_allow: false,
        error_img: false,
        error_msg: false,


    },
    mounted() {
        this.img_show();
    },
    methods: {
        ssm_code() {
            if (this.inte === true) {
                return;
            }
            this.inte = true;


            let url = "/sms_codes/" + this.mobile + "?img_code=" + this.img_db + "&uuid=" + this.uuid;
            if (this.mobile.length === 0) {
                this.check_mobile();

            }

            axios.get(url, {responseType: "json"})
                .then(response => {
                    if (response.data.code === "0") {
                        let num = 60;
                        let t = setInterval(() => {
                            if (num === 1) {
//
                                clearInterval(t);
                                this.ssm_code_message = "发送";
                                this.inte = false;
                            } else {
                                num -= 1;
                                this.ssm_code_message = num;
                            }
                        }, 1000);

                    } else {
                        if (response.data.code === 1) {
                            this.error_img_message = response.data.errmsg;
                            this.error_img = true;
                        } else {
                            this.error_message_msg = response.data.errmsg;
                            this.error_msg = true
                        }

                    }
                    ;

                })
                .catch(error => {
                    console.log(error)
                })

        },
        check_msg() {
            let error_msg;
            error_msg = this.msg.length !== 6;
        },


        img_show() {
            this.uuid = generateUUID();
            this.img_code_url = "/image_codes/" + this.uuid;
        },
        check_img() {
            if (this.img_db.length !== 4) {
                this.error_img_message = "img_code:NOne";
                this.error_img = true;
            } else {
                this.error_img = false;
            }

        },
        check_username() {
//                            username : len{5:20} range[0-9A-Za-z_-]

            let re = /^[0-9A-Za-z_-]{5,20}$/;
            if (re.test(this.username)) {
                this.error_name = false;
//                                                                            this.error_name_message = "unique user register"
            } else {
                this.error_name_message = "用户长度错误";
                this.error_name = true;

            }
            if (this.error_name === false) {
                let url = "/usernames/" + this.username + "/count"
                axios.get(url, {"responseType": "json"})
                    .then(response => {

                        if (response.data.count >= 1) {
                            this.error_name_message = "用户名已存在";
                            this.error_name = true;
                        } else {
                            this.error_name = this.error_name;
                        }

                    })
                    .catch(error => {
                        console.log(error.response);

                    })
            }


        },
        check_password() {
            this.error_pass = true;
            let re = /^[0-9A-Za-z]{6,12}$/
            if (this.password === "") {
                this.error_pass_message = "密码不能为空";
                return
            }
            if (!re.test(this.password)) {
                this.error_pass_message = "密码格式错误"
                return;
            }
            this.error_pass = false
        },
        check_password2() {
            this.error_pass2 = this.password !== this.password2;
        },
        check_mobile() {
            let re = /^1[3-9]\d{9}$/
            if (re.test(this.mobile)) {
                this.error_phone = false;
            } else {
                this.error_phone_massage = "手机号格式错误";
                this.error_phone = true;
            }
            if (this.error_phone === false) {
                let ual = "/phone/" + this.mobile + "/count";
                axios.get(ual, {"responseType": "json"})
                    .then(response => {
                        if (response.data.count === 1) {
                            this.error_phone_massage = "手机号已存在";
                            this.error_phone = true;
                        }

                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }

        },
        check_allow() {
            this.error_allow = !this.allow;

        },
        on_submit() {
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_allow();
            if (this.error_username === true || this.error_pass === true || this.error_pass2 === true || this.error_phone === true || this.error_allow === true || this.error_allow == true) {
                window.event.returnValue = false;
            }
// //                                            else{
//    //                                                    window.event.returnValue =false;
//                                                    alter("commit TRUE");
//                                                }


        },
    },

})