/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
    "../../templates/**/*.html",
    "../js/*.js",
    "../../../static/node_modules/flowbite/**/*.js",],
  theme: {
    extend: {
      fontFamily: {
        sans: ['InterVariable', ...defaultTheme.fontFamily.sans],
      },
    },
    screens : {
      'xs' : '540px',
      'sm' : '640px',
      'md' : '768px',
      'lg' : '1024px',
      'xl' : '1280px',
      '2xl': '1536px',
    }
  },
  plugins: [
    require('../../../static/node_modules/flowbite/plugin'),
    require('../../../static/node_modules/daisyui/'),
    function({ addUtilities }) {
      const newUtilities = {
        '.hover-anim': {
          transition : '300ms ease-in-out',
        },
        '.no-scrollbar::-webkit-scrollbar': {
          display: 'none',
        },
        '.no-scrollbar': {
          '-ms-overflow-style': 'none', // IE and Edge
          'scrollbar-width': 'none',    // Firefox
        },
      };

      addUtilities(newUtilities, ['responsive', 'hover']);
    },
  ],
  safelist: [
    // Kadang kadang gak ke compile sama tailwind kalo ditaronya cuma di js nya
  
    // Opacity class
    // 'opacity-0',
    // 'opacity-5',
    // 'opacity-10',
    // 'opacity-20',
    // 'opacity-25',
    // 'opacity-30',
    // 'opacity-40',
    // 'opacity-50',
    // 'opacity-60',
    // 'opacity-70',
    // 'opacity-75',
    // 'opacity-80',
    // 'opacity-90',
    // 'opacity-95',
    // 'opacity-100',
  
    // // Background opacity class
    // 'bg-opacity-0',
    // 'bg-opacity-5',
    // 'bg-opacity-10',
    // 'bg-opacity-20',
    // 'bg-opacity-25',
    // 'bg-opacity-30',
    // 'bg-opacity-40',
    // 'bg-opacity-50',
    // 'bg-opacity-60',
    // 'bg-opacity-70',
    // 'bg-opacity-75',
    // 'bg-opacity-80',
    // 'bg-opacity-90',
    // 'bg-opacity-95',
    // 'bg-opacity-100',
  
    // // Rotate class
    // 'rotate-0',
    // 'rotate-1',
    // 'rotate-2',
    // 'rotate-3',
    // 'rotate-6',
    // 'rotate-12',
    // 'rotate-45',
    // 'rotate-90',
    // 'rotate-180',
    // 'rotate-270',
  
    // // Translate class
    // 'translate-x-0',
    // 'translate-x-1',
    // 'translate-x-2',
    // 'translate-x-3',
    // 'translate-x-4',
    // 'translate-x-5',
    // 'translate-x-6',
    // 'translate-x-7',
    // 'translate-x-8',
    // 'translate-x-9',
    // 'translate-x-10',
    // 'translate-x-11',
    // 'translate-x-12',
    // 'translate-x-full',
  
    // 'translate-y-0',
    // 'translate-y-1',
    // 'translate-y-2',
    // 'translate-y-3',
    // 'translate-y-4',
    // 'translate-y-5',
    // 'translate-y-6',
    // 'translate-y-7',
    // 'translate-y-8',
    // 'translate-y-9',
    // 'translate-y-10',
    // 'translate-y-11',
    // 'translate-y-12',
    // 'translate-y-full',

    // // Text colors
    // ...['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'].flatMap(shade => [
    //   `text-gray-${shade}`,
    //   `text-red-${shade}`,
    //   `text-yellow-${shade}`,
    //   `text-green-${shade}`,
    //   `text-blue-${shade}`,
    //   `text-indigo-${shade}`,
    //   `text-purple-${shade}`,
    //   `text-pink-${shade}`,
    //   `text-rose-${shade}`,
    // ]),

    // // Background colors
    // ...['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'].flatMap(shade => [
    //   `bg-gray-${shade}`,
    //   `bg-red-${shade}`,
    //   `bg-yellow-${shade}`,
    //   `bg-green-${shade}`,
    //   `bg-blue-${shade}`,
    //   `bg-indigo-${shade}`,
    //   `bg-purple-${shade}`,
    //   `bg-pink-${shade}`,
    //   `bg-rose-${shade}`,
    // ]),

    // // Border colors
    // ...['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'].flatMap(shade => [
    //   `border-gray-${shade}`,
    //   `border-red-${shade}`,
    //   `border-yellow-${shade}`,
    //   `border-green-${shade}`,
    //   `border-blue-${shade}`,
    //   `border-indigo-${shade}`,
    //   `border-purple-${shade}`,
    //   `border-pink-${shade}`,
    //   `border-rose-${shade}`,
    // ]),
  ],
  
}

