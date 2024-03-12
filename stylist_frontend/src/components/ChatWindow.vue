<template>
  <div class="chat-window h-screen">
    <vue-advanced-chat 
      .messages="messages" 
      .options="options"
      .rooms="[{ roomId: 'main', roomName: 'Stylist Chat', avatar: '/images/logo.svg', users: [currentUser]}]" 
      :rooms-list-opened="false"
      :rooms-loaded="true"
      :messages-loaded="true"
      :current-user-id="currentUser._id"
      accepted-files=".png, .jpg, .jpeg"
      show-audio="false"
      @send-message="onInputSubmit" 
      .message-actions="[{
        label: 'Send',
        action: (message: Message) => {
          console.log('Send message ' + message.content);
        },
      }]"
      v-bind="{ 
        'current-user-id': currentUser?._id || '',
        'room-info-enabled': false,
       }" 

       />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, Ref } from "vue";
import { VueAdvancedChat, Message, register, RoomUser } from "vue-advanced-chat";
register();
import { v4 as uuidv4 } from "uuid";

function toTimeString(date: Date): string {
  let month = date.toLocaleString('default', { month: 'short' });
  return `${date.getFullYear()}-${month}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}`;
}

export default defineComponent({
  name: "ChatWindow",
  components: {
    VueAdvancedChat,
  },
  setup() {
    // Define the current user, the messages, and the options for the chat component
    const currentUser: Ref<RoomUser> = ref({
      _id: "user",
      username: "User",
      avatar: "",
      status: { state: "online", lastChanged: new Date().toDateString()},
    });
    const messages: Ref<Array<Message>> = ref([]);
    const options = ref({
      enableVoiceMessages: false,
      enableReactions: false,
      enableSeenBy: false,
      enableLinkPreview: false,
      enableUploads: true,
      enableAttachments: false,
      enableReply: true,
      enableEdit: false,
      enableDelete: false,
      enableGroup: false,
      enableSearch: false,
      enableOptions: false,
      enableScrollToBottom: true,
      enableScrollToTop: false,
      enableLoadMore: false,
      enableComposer: true,
      enableInput: true,
      enableSendButton: true,
      enableEmojis: false,
      enableRecording: false,
      enableMarkdown: true,
      enableTypingIndicator: true,
      enableOnlinePresence: false,
      enableCustomTheme: true,
      enableRooms: false,
      customTheme: {
        primaryColor: "#333333",
        secondaryColor: "#f0f0f0",
        tertiaryColor: "#ffffff",
        quaternaryColor: "#e0e0e0",
        quinaryColor: "#999999",
        senaryColor: "#666666",
        septenaryColor: "#333333",
        octonaryColor: "#f0f0f0",
        nonaryColor: "#ffffff",
        denaryColor: "#e0e0e0",
      },
    });

    // update the image preview in the chat message after it's uploaded
    const updateMessageImage = (newMessage: Message, url: string) => {
      const existingMessage = messages.value.find(m => m._id === newMessage._id);
      // update the URL of the first message file
      const message = existingMessage || newMessage;

      if(message && message.files && message.files.length > 0) {
        message.files[0].url = url;
        const existingMessages = messages.value.filter(m => m._id !== message._id);
        //set a new message ID to prevent file from being overwritten
        message._id = uuidv4();
        messages.value = [...existingMessages, message];
      } 
    }

    const onInputSubmit = async (event: CustomEvent) => {
      // Create a new message object with the content and the current user
      console.log("called!")
      let content = event.detail[0].content;
      let files = event.detail[0].files;
      const newMessage: Message = {
        // generate uuid
        _id: uuidv4(),
        content,
        senderId: currentUser.value._id,
        date: new Date().toLocaleString('default', { year: 'numeric', month: 'short', day: 'numeric' }),
        timestamp: toTimeString(new Date()),
      };

      if(files) {
        newMessage.files = [...files.map((file: any) => {
          var messageFile = {
            name: file.name,
            size: file.size,
            type: file.type,
            url: file.url || file.localUrl,
            extension: file.extension,
            preview: file.localUrl,
          }
          const reader = new FileReader();
          reader.readAsDataURL(file.blob);
          
          reader.onload = () => {
            // Get the base64-encoded string from the reader result
            messageFile.url = reader.result as string;
            // reload messages so UI updates
            messages.value = [...messages.value];
            updateMessageImage(newMessage, messageFile.url!);
            callBackendFunction(content, reader.result as string);
          };
          return messageFile;
        })];
      } else {

        // Push the new message to the messages array
        messages.value = [...messages.value, newMessage];
        // Call the backend function to get the response from the stylist bot
        callBackendFunction(content, "");
      }
    };

    const callBackendFunction = async (prompt: string, image: string) => {
      // Get the previous prompts and responses from the messages array
      const context = messages.value
        .filter((message) => message.content || message.replyMessage)
        .map((message) => ({
          prompt: message.content,
          response: message.replyMessage,
        }));
      // Create a JSON object with the prompt, the image, and the context
      const data = {
        prompt,
        image,
        context,
      };
      // Send a POST request to the backend function URL with the data
      const response = await fetch("<backend function URL>", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      // Get the response data from the fetch response
      const responseData = await response.json();
      // Create a new message object with the response data and the stylist bot
      const newMessage: Message = {
        _id: uuidv4(),
        content: responseData.response,
        files: responseData.images,
        senderId: "stylist-bot",
        date: new Date().toLocaleString('default', { year: 'numeric', month: 'short', day: 'numeric' }),
        timestamp: toTimeString(new Date()),
      };
      // Push the new message to the messages array
      messages.value = [...messages.value, newMessage];
    };

    // Return the current user, the messages, the options, and the event handlers
    return {
      currentUser,
      messages,
      options,
      onInputSubmit,
    };
  },
  
  mounted() {
    // Add a welcome message from the stylist bot when the component is mounted
    this.messages = [...this.messages, { _id: "stylist-bot", content: "Hello! I'm your virtual stylist chatbot. You can ask me for fashion advice, recommendations, and more. You can also upload images of clothing items and accessories to get personalized suggestions. How can I help you today?", senderId: "stylist-bot", date: new Date().toTimeString()}];
  },
});

</script>
  
<style scoped>
.chat-window {
  @apply h-screen flex-1 overflow-y-auto;
}
</style>
  