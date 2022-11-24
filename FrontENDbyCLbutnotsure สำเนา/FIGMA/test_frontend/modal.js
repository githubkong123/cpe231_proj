/* Please ❤ this */
new Vue({
    el: "#app",
    data: {
        CLASSNAME_WRAPPER: 'active',
        showDialog: false,
        classDialog: '',
    },
    methods: {
        generateDialog() {
            this.showDialog = true;
            setTimeout(() => {
                this.classDialog = this.CLASSNAME_WRAPPER;
            }, 100)
        },
        closeDialog() {
            this.classDialog = '';
            setTimeout(() => {
                this.showDialog = false;
            }, 100)
        }
    }
});