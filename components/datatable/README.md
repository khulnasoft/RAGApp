<div align="center" markdown="1">

<img width="80" alt="datatable-logo" src="https://github.com/user-attachments/assets/8235f4b9-993a-4329-97de-9431dcf63aae" >

<h1>Ragapp DataTable</h1>

**A modern datatable library for the web**

[![Test and Release](https://github.com/khulnasoft/ragapp/workflows/Test%20and%20Release/badge.svg)](https://github.com/khulnasoft/ragapp/actions?query=workflow%3A%22Test+and+Release%22)
[![npm version](https://badge.fury.io/js/ragapp-datatable.svg)](https://badge.fury.io/js/ragapp-datatable)
![npm bundle size (minified + gzip)](https://img.shields.io/bundlephobia/minzip/ragapp-datatable.svg)


![datatable-demo-2](https://user-images.githubusercontent.com/9355208/40740030-5412aa40-6465-11e8-8542-b0247ab1daac.gif)

</div>

## Ragapp Datatable

Ragapp DataTable is a simple, modern and interactive datatable library for displaying tabular data. Originally built for [NxERP](https://github.com/khulnasoft-lab/nxerp), it can be used to render large amount of rows without sacrificing performance and has the basic data grid features like inline editing and keyboard navigation. It does not require jQuery, unlike most data grids out there.

### Motivation

I was trying to remove all legacy UI components from the [ragapp](https://github.com/khulnasoft/ragapp) codebase. We were using [SlickGrid](https://github.com/mleibman/SlickGrid) for rendering tables. It was unmaintained and UI was dated. Other datatable solutions either didn't have the features we needed or were closed source. So we built our own.


### Key Features

- **Cell**: Enable editing within individual cells and features like custom formatters, inline editing, and mouse selection. Users can easily copy cell content, navigate through cells using the keyboard, and take advantage of a custom cell editor for advanced functionality.
- **Column**: Columns are highly flexible, allowing users to reorder, resize, and sort them with ease. Additional features include hiding/removing columns and adding custom actions.
- **Row**: Rows support advanced interactions, including row selection, tree-structured organization, and inline filters for precise control. They handle large datasets efficiently with dynamic row heights.


## Usage

```bash
yarn add ragapp-datatable
# or
npm install ragapp-datatable
```

> Note: [`sortablejs`](https://github.com/RubaXa/Sortable) is required to be installed as well.


```js
const datatable = new DataTable('#datatable', {
  columns: [ 'First Name', 'Last Name', 'Position' ],
  data: [
    [ 'Don', 'Joe', 'Designer' ],
    [ 'Mary', 'Jane', 'Software Developer' ]
  ]
});
```

## Development Setup

* `yarn start` - Start dev server
* Open `index.html` located in the root folder, and start development.
* Run `yarn lint` before committing changes
* This project uses [commitizen](https://github.com/commitizen/cz-cli) for conventional commit messages, use `yarn commit` command instead of `git commit`

## Links

- [Making a new datatable for the web](https://medium.com/ragapp%C3%A9-thoughts/things-i-learned-building-a-library-for-the-web-6846a588bf53)

<br>
<br>
<div align="center" style="padding-top: 0.75rem;">
	<a href="https://ragapp.io" target="_blank">
		<picture>
			<source media="(prefers-color-scheme: dark)" srcset="https://ragapp.io/files/Ragapp-white.png">
			<img src="https://ragapp.io/files/Ragapp-black.png" alt="Ragapp Technologies" height="28"/>
		</picture>
	</a>
</div>
