<template>
  <div v-if="editor" class="">
    <div class="control-group">
      <div class="button-group">
        <button
          @click="editor.chain().focus().toggleBold().run()"
          :disabled="!editor.can().chain().focus().toggleBold().run()"
          :class="[editor.isActive('bold') ? 'is-active' : '', 'editor-btn']"
        >
          Bold
        </button>
        <button
          @click="editor.chain().focus().toggleItalic().run()"
          :disabled="!editor.can().chain().focus().toggleItalic().run()"
          :class="[editor.isActive('italic') ? 'is-active' : '', 'editor-btn']"
        >
          Italic
        </button>
        <button
          @click="editor.chain().focus().toggleStrike().run()"
          :disabled="!editor.can().chain().focus().toggleStrike().run()"
          :class="[editor.isActive('strike') ? 'is-active' : '', 'editor-btn']"
        >
          Strike
        </button>
        <button
          @click="editor.chain().focus().unsetAllMarks().run()"
          class="editor-btn"
        >
          Clear Styling
        </button>
        <button
          @click="editor.chain().focus().clearNodes().run()"
          class="editor-btn"
        >
          Clear Formatting
        </button>
        <button
          @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
          :class="[
            editor.isActive('heading', { level: 1 }) ? 'is-active' : '',
            'editor-btn',
          ]"
        >
          H1
        </button>
        <button
          @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
          :class="[
            editor.isActive('heading', { level: 2 }) ? 'is-active' : '',
            'editor-btn',
          ]"
        >
          H2
        </button>
        <button
          @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
          :class="[
            editor.isActive('heading', { level: 3 }) ? 'is-active' : '',
            'editor-btn',
          ]"
        >
          H3
        </button>
        <button
          @click="editor.chain().focus().toggleHeading({ level: 4 }).run()"
          :class="[
            editor.isActive('heading', { level: 4 }) ? 'is-active' : '',
            'editor-btn',
          ]"
        >
          H4
        </button>
        <button
          @click="editor.chain().focus().toggleHeading({ level: 5 }).run()"
          :class="[
            editor.isActive('heading', { level: 5 }) ? 'is-active' : '',
            'editor-btn',
          ]"
        >
          H5
        </button>
        <button
          @click="editor.chain().focus().toggleHeading({ level: 6 }).run()"
          :class="[
            editor.isActive('heading', { level: 6 }) ? 'is-active' : '',
            'editor-btn',
          ]"
        >
          H6
        </button>
        <button
          @click="editor.chain().focus().toggleBulletList().run()"
          :class="[
            editor.isActive('bulletList') ? 'is-active' : '',
            'editor-btn',
          ]"
        >
          Bullet list
        </button>
        <button
          @click="editor.chain().focus().toggleOrderedList().run()"
          :class="[
            editor.isActive('orderedList') ? 'is-active' : '',
            'editor-btn',
          ]"
        >
          Numbered list
        </button>
        <button
          @click="editor.chain().focus().setHorizontalRule().run()"
          class="editor-btn"
        >
          Horizontal rule
        </button>
        <button
          @click="setLink"
          :class="{ 'is-active': editor.isActive('link') }"
          class="editor-btn"
        >
          Add link
        </button>
        <button
          @click="editor.chain().focus().unsetLink().run()"
          :disabled="!editor.isActive('link')"
          class="editor-btn"
        >
          Remove link
        </button>
        <button
          @click="editor.chain().focus().undo().run()"
          :disabled="!editor.can().chain().focus().undo().run()"
          class="editor-btn"
        >
          Undo
        </button>
        <button
          @click="editor.chain().focus().redo().run()"
          :disabled="!editor.can().chain().focus().redo().run()"
          class="editor-btn"
        >
          Redo
        </button>
      </div>
    </div>
    <editor-content :editor="editor" />
  </div>
</template>

<script>
import Link from '@tiptap/extension-link';
import { ListItem } from '@tiptap/extension-list';
import { Color, TextStyle } from '@tiptap/extension-text-style';
import StarterKit from '@tiptap/starter-kit';
import { Editor, EditorContent } from '@tiptap/vue-3';

export default {
  name: 'RichEditor',
  components: {
    EditorContent,
  },
  props: { model_value: String },
  data() {
    return {
      editor: null,
    };
  },
  mounted() {
    this.editor = new Editor({
      extensions: [
        Color.configure({ types: [TextStyle.name, ListItem.name] }),
        TextStyle.configure({ types: [ListItem.name] }),
        StarterKit,
        Link.configure({
          openOnClick: false,
          defaultProtocol: 'https',
        }),
      ],
      content: this.model_value,
      onUpdate: ({ editor }) => {
        const html = editor.getHTML();
        this.$emit('update:model_value', html);
      },
    });
  },
  methods: {
    setLink() {
      const previousUrl = this.editor.getAttributes('link').href;
      const url = window.prompt('URL', previousUrl);

      // cancelled
      if (url === null) {
        return;
      }

      // empty
      if (url === '') {
        this.editor.chain().focus().extendMarkRange('link').unsetLink().run();

        return;
      }

      // update link
      this.editor
        .chain()
        .focus()
        .extendMarkRange('link')
        .setLink({ href: url })
        .run();
    },
    addIframe() {
      const url = window.prompt('URL');

      if (url) {
        this.editor.chain().focus().setIframe({ src: url }).run();
      }
    },
  },
  beforeUnmount() {
    this.editor.destroy();
  },
};
</script>

<style>
.ProseMirror {
  border: 1px solid black;
  border-radius: 4px;
  padding: 4px;
}

.editor-btn {
  background-color: lightgray;
  border-radius: 4px;
  border: none;
  margin: 2px;
}
</style>
