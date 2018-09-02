let menuButton = new Vue({
    el: "#menuButton",
    data: {}
});

let tableBodyTags = new Vue({
    el: "#tableBodyTags",
    data: {
        rows: [
            {id:1, theme:"Python", totalViews: 12453},
            {id:2, theme:"Django", totalViews: 9084},
            {id:3, theme:"TensorFlow", totalViews: 8173}
        ]
    }
});

let tableBodyMembers = new Vue({
    el: "#tableBodyMembers",
    data: {
        rows: [
            {id:1, nickname: "lexani42", contributions: 241},
            {id:2, nickname: "Rivera", contributions: 180},
            {id:3, nickname: "ChipX", contributions: 173}
        ]
    }
});

let userShortcut = new Vue({
    el: "#userShortcut",
    data: {}
});

let issueComment = new Vue({

});