import axios from 'axios'
import Cookies from 'js-cookie'
import './modal.css'

const API_URL = 'http://127.0.0.1:32030'
const DEFAULT_OPTIONS = {}
const REQUIRED_FIELDS = ['departure', 'destination', 'callsign', 'route']

export class Plan {
  constructor (plan, options = {}) {
    this.buttons = []

    for (const field of REQUIRED_FIELDS) {
      if (!(field in plan)) {
        throw new Error('Missing required field: ' + field)
      }
    }
    this.plan = plan

    const defaultOptions = Object.assign({}, DEFAULT_OPTIONS)
    this.options = Object.assign(defaultOptions, options)

    this.applyOptions()
    console.log('FSFPL Flight Plan Ready.')
  }

  applyOptions () {
    console.log(this.options)
    // Add buttons.
    if ('buttons' in this.options) {
      for (const button of this.options.buttons) {
        this.createButton(button)
      }
    }
  }

  createButton (buttonOptions) {
    const button = document.createElement('button')
    button.onclick = this.send.bind(this)

    const wrapper = document.getElementById(buttonOptions.to)
    const text = document.createTextNode(buttonOptions.text)
    button.appendChild(text)
    button.setAttribute('defaultText', buttonOptions.text)
    wrapper.appendChild(button)

    this.buttons.push(button)
  }

  resetButtonTexts () {
    for (const button of this.buttons) {
      button.innerHTML = button.getAttribute('defaultText')
    }
  }

  printToButtons (text) {
    for (const button of this.buttons) {
      button.innerHTML = text
    }
  }

  modal (content) {
    const modal = document.getElementById('FSFPL-modal')
    if (modal === null) {
      return this.createModal(content)
    }
    const contentDiv = document.getElementById('FSFPL-modal-content')
    contentDiv.innerHTML = content
    modal.style.display = 'block'
  }

  createModal (content) {
    const modal = document.createElement('div')
    modal.setAttribute('id', 'FSFPL-modal')
    const closeButton = document.createElement('button')
    const closeButtonText = document.createTextNode('X')
    closeButton.appendChild(closeButtonText)
    closeButton.onclick = this.closeModal.bind(this)
    const modalContent = `<div id="FSFPL-modal-wrapper">
      <div id="FSFPL-modal-button"></div>
      <div id="FSFPL-modal-inside">
        <div id="FSFPL-modal-content">
          ${content}
        </div>
      </div>
    </div>`

    modal.innerHTML = modalContent
    document.body.appendChild(modal)

    document.getElementById('FSFPL-modal-button').appendChild(closeButton)
  }

  closeModal () {
    const modal = document.getElementById('FSFPL-modal')
    modal.style.display = 'none'
  }

  resetPinCookie () {
    Cookies.remove('FSFPL_PIN')
  }

  getPin (useCookie = true) {
    let pin = Cookies.get('FSFPL_PIN')
    if (pin !== undefined || !useCookie) {
      return pin
    } else {
      pin = this.askPin()
      Cookies.set('FSFPL_PIN', pin)
      return pin
    }
  }

  askPin () {
    const pin = prompt('Enter your FS Flight Plan Link PIN code.')
    return pin
  }

  async send () {
    console.log('sending...')
    const pin = this.getPin()
    await axios({
      url: API_URL + '/plan',
      method: 'post',
      data: {
        plan: this.plan
      },
      auth: {
        username: 'User',
        password: pin
      }
    })
      .then(result => {
        console.log(result)
        this.modal('Flight Plan Sended to Desktop.')
      })
      .catch(error => {
        console.error(error)
        if (error.response.status === 401) {
          this.resetPinCookie()
          this.modal('Wrong Pin.')
        }
      })
  }
}

console.log('FSFPL client is loaded.')
