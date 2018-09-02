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
    el: "#issueComment",
    data: {
        commentators: [
            {nickname: "Annaid", avatar:"img_avatar1.png", text: "Your problem is that the first sentence and the second sentence's introductory clause are past tense, then \"so far\" slips into present tense. It \"is\" still the first day (if I understand correctly), and you need a comma after fugitive. Also, you could change lay to lie, like a present tense narrative. Lastly, referring to the edit of the last word...your original word (that began with an F) seemed way better to me, more natural and authentic for your character, like someone who would use that word casually and almost exclusively to mean mistake, not necessarily a big one."},
            {nickname: "Nal", avatar:"img_avatar2.png", text: "Over the years, many tools and modeling methodologies have been developed to assist in designing software systems. One of the most popular tools in use today is Unified Modeling Language (UML). Although it is beyond the scope of this book to describe UML in fine detail,we will use UML class diagrams to illustrate the classes that we build."},
            {nickname: "Jeu", avatar:"img_avatar3.png", text: "It's odd, but if I were to say this with the full words, I would say, One of the most popular tools is the Unified Modeling Language (and include the article). However, if I were to use the acronym, I'd probably say, One of the most popular tools is UML (not the UML). A similar phenomenon often happens with school names. He has a master's degree from MIT. He has a master's degree from the Massachusetts Institute of Technology. Bottom line: article usage can be tricky and inconsistant with acronyms."},
            {nickname: "Olllobeby", avatar:"img_avatar4.png", text: "The original drywall was removed up to where the tile stopped and shim stock was placed on the edges of the studs so that the outer surface of the new backer lined up with the 1/2\" drywall above it. But the blocking for grab bars was put in before the shims and was lined up with the studs. I don't remember if shim stock was placed on the blocking so, between the studs, there was, or could have been, a slight gap between the backer and the blocking.\n" +
                    "\n" +
                    "Some years later I installed grab bars with screws into the blocking and had to be careful not to screw in too tight. I later realized I could have squirted silicone caulk onto the holes in the tile to overflow into the air gap and so provided support for the grab bars."}
        ]
    }
});