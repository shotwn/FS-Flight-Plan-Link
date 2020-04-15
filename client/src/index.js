import axios from 'axios'
import Cookies from 'js-cookie'
import './modal.css'

const API_URL = 'http://127.0.0.1:32030'
const DEFAULT_OPTIONS = {}
const REQUIRED_FIELDS = ['departure', 'destination', 'callsign', 'route']

export class Plan {
  constructor (plan, options = {}, parent = null) {
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
    button.onclick = () => {
      const opt = {
        caller: button
      }
      this.send(opt)
    }

    const wrapper = document.getElementById(buttonOptions.to)
    const text = document.createTextNode(buttonOptions.text)
    button.appendChild(text)
    button.setAttribute('defaultText', buttonOptions.text)
    wrapper.appendChild(button)

    this.buttons.push(button)
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
      <div style="display: inline-block; padding: 10px;">FS Flight Plan Link Client</div>
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

  setCallerDisabled (caller, flag) {
    if (caller === undefined) {
      return
    }

    if (flag) {
      caller.setAttribute('disabled', true)
    } else {
      caller.removeAttribute('disabled')
    }
  }

  async send (options = {}) {
    // console.log('sending...')
    this.setCallerDisabled(options.caller, true)

    const pin = this.getPin()
    return await axios({
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
        return true
      })
      .catch(error => {
        if (error.response === undefined || error.response.status === 404) {
          this.modal('Couldn\'t reach FS Flight Plan Link.<br>Are you sure desktop software is running ?')
          return false
        }
        if (error.response.status === 401) {
          this.resetPinCookie()
          this.modal('Wrong Pin.')
          return false
        }
      })
      .then(result => {
        this.setCallerDisabled(options.caller, false)
        return result
      })
  }
}

export class Utility {
  constructor (options = {}) {
    const defaultOptions = Object.assign({}, DEFAULT_OPTIONS)
    this.options = Object.assign(defaultOptions, options)
  }

  /**
   * @typedef {'innerHTML' | 'value'} MappingAttribute
   */
  /**
   * @typedef {Object} MappingEntry
   * @property {string} selector
   * @property {MappingAttribute} attribute
   */
  /**
   * @typedef {Object} Mapping
   * @property {MappingEntry} key - A mapping entry.
   */
  /**
   * Collect data from DOM elements.
   * Match key to flight plan field.
   * @param {Mapping} mapping
   * @example
   * collector({
   *  departure: {
   *    selector: '#mydiv-departure',
   *    attribute: 'innerHTML'
   *  },
   *  destination: {
   *    selector: '#myinput-destination',
   *    attribute: 'value'
   *  }
   * })
   */
  async collect (mapping) {
    const collectedPlanFields = {}
    for (const [planField, mappingEntry] of Object.entries(mapping)) {
      // FUNCTION based.
      if (mappingEntry.func !== undefined) {
        mappingEntry.key = planField
        collectedPlanFields[planField] = mappingEntry(mappingEntry)
        continue
      }

      // selector / attribute based.
      const domElement = document.querySelector(mappingEntry.selector)
      if (domElement === undefined) {
        console.error('No elements selected for ' + mappingEntry.selector)
        continue
      }

      let value
      if (mappingEntry.attribute === 'innerHTML') {
        value = domElement.innerHTML
      } else {
        value = domElement.getAttribute(mappingEntry.attribute)
      }

      collectedPlanFields[planField] = value
    }
    return collectedPlanFields
  }

  async send (planFields, options) {
    const newPlan = new Plan(planFields, this.options)

    return await newPlan.send(options)
  }
}

console.log('FSFPL client is loaded.')
