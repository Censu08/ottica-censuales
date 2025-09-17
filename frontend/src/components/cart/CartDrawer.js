'use client'
import { Fragment } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { XMarkIcon, ShoppingCartIcon } from '@heroicons/react/24/outline'
import { useSelector, useDispatch } from 'react-redux'
import { removeItem, updateQuantity } from '@/store/slices/cartSlice'
import Image from 'next/image'
import Link from 'next/link'

export default function CartDrawer({ isOpen, onClose }) {
  const dispatch = useDispatch()
  const { items, total, itemsCount } = useSelector((state) => state.cart)

  const handleRemoveItem = (productId, variantId) => {
    dispatch(removeItem({ productId, variantId }))
  }

  const handleUpdateQuantity = (productId, variantId, quantity) => {
    if (quantity <= 0) {
      handleRemoveItem(productId, variantId)
    } else {
      dispatch(updateQuantity({ productId, variantId, quantity }))
    }
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('it-IT', {
      style: 'currency',
      currency: 'EUR'
    }).format(price)
  }

  return (
    <Transition.Root show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-in-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in-out duration-300"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-hidden">
          <div className="absolute inset-0 overflow-hidden">
            <div className="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10">
              <Transition.Child
                as={Fragment}
                enter="transform transition ease-in-out duration-300 sm:duration-700"
                enterFrom="translate-x-full"
                enterTo="translate-x-0"
                leave="transform transition ease-in-out duration-300 sm:duration-700"
                leaveFrom="translate-x-0"
                leaveTo="translate-x-full"
              >
                <Dialog.Panel className="pointer-events-auto w-screen max-w-md">
                  <div className="flex h-full flex-col overflow-y-scroll bg-white shadow-xl">
                    <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-6">
                      <div className="flex items-start justify-between">
                        <Dialog.Title className="text-lg font-medium text-gray-900">
                          Carrello ({itemsCount} {itemsCount === 1 ? 'articolo' : 'articoli'})
                        </Dialog.Title>
                        <div className="ml-3 flex h-7 items-center">
                          <button
                            type="button"
                            className="relative -m-2 p-2 text-gray-400 hover:text-gray-500"
                            onClick={onClose}
                          >
                            <XMarkIcon className="h-6 w-6" />
                          </button>
                        </div>
                      </div>

                      <div className="mt-8">
                        {items.length === 0 ? (
                          <div className="text-center py-12">
                            <ShoppingCartIcon className="mx-auto h-12 w-12 text-gray-400" />
                            <h3 className="mt-2 text-sm font-medium text-gray-900">Il carrello è vuoto</h3>
                            <p className="mt-1 text-sm text-gray-500">
                              Inizia ad aggiungere prodotti per procedere con l'acquisto
                            </p>
                          </div>
                        ) : (
                          <div className="flow-root">
                            <ul role="list" className="-my-6 divide-y divide-gray-200">
                              {items.map((item) => (
                                <li key={`${item.product.id}-${item.variant?.id || 'no-variant'}`} className="flex py-6">
                                  <div className="h-24 w-24 flex-shrink-0 overflow-hidden rounded-md border border-gray-200">
                                    {item.product.main_image ? (
                                      <Image
                                        src={item.product.main_image}
                                        alt={item.product.name}
                                        width={96}
                                        height={96}
                                        className="h-full w-full object-cover object-center"
                                      />
                                    ) : (
                                      <div className="h-full w-full bg-gray-100 flex items-center justify-center">
                                        <ShoppingCartIcon className="h-8 w-8 text-gray-400" />
                                      </div>
                                    )}
                                  </div>

                                  <div className="ml-4 flex flex-1 flex-col">
                                    <div>
                                      <div className="flex justify-between text-base font-medium text-gray-900">
                                        <h3>
                                          <Link href={`/prodotti/${item.product.slug}`}>
                                            {item.product.name}
                                          </Link>
                                        </h3>
                                        <p className="ml-4">{formatPrice(item.price)}</p>
                                      </div>
                                      <p className="mt-1 text-sm text-gray-500">{item.product.brand?.name}</p>
                                      {item.variant && (
                                        <p className="mt-1 text-sm text-gray-500">{item.variant.name}</p>
                                      )}
                                    </div>
                                    <div className="flex flex-1 items-end justify-between text-sm">
                                      <div className="flex items-center space-x-2">
                                        <button
                                          onClick={() => handleUpdateQuantity(item.product.id, item.variant?.id, item.quantity - 1)}
                                          className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50"
                                        >
                                          -
                                        </button>
                                        <span className="text-gray-700 font-medium">{item.quantity}</span>
                                        <button
                                          onClick={() => handleUpdateQuantity(item.product.id, item.variant?.id, item.quantity + 1)}
                                          className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50"
                                        >
                                          +
                                        </button>
                                      </div>

                                      <div className="flex">
                                        <button
                                          type="button"
                                          onClick={() => handleRemoveItem(item.product.id, item.variant?.id)}
                                          className="font-medium text-primary-600 hover:text-primary-500"
                                        >
                                          Rimuovi
                                        </button>
                                      </div>
                                    </div>
                                  </div>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>

                    {items.length > 0 && (
                      <div className="border-t border-gray-200 px-4 py-6 sm:px-6">
                        <div className="flex justify-between text-base font-medium text-gray-900">
                          <p>Totale</p>
                          <p>{formatPrice(total)}</p>
                        </div>
                        <p className="mt-0.5 text-sm text-gray-500">
                          Spese di spedizione calcolate al checkout
                        </p>
                        <div className="mt-6">
                          <Link
                            href="/checkout"
                            onClick={onClose}
                            className="flex justify-center items-center px-6 py-3 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-primary-600 hover:bg-primary-700 w-full"
                          >
                            Procedi al checkout
                          </Link>
                        </div>
                        <div className="mt-6 flex justify-center text-center text-sm text-gray-500">
                          <p>
                            oppure{' '}
                            <button
                              type="button"
                              className="font-medium text-primary-600 hover:text-primary-500"
                              onClick={onClose}
                            >
                              Continua lo shopping
                            </button>
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  )
}
