import { useLayoutEffect, useRef, type ReactNode } from 'react'

export function Modal({
  titleId,
  busy,
  onCancel,
  children,
}: {
  titleId: string
  busy: boolean
  onCancel: () => void
  children: ReactNode
}) {
  const element = useRef<HTMLDialogElement>(null)
  useLayoutEffect(() => {
    const dialog = element.current!
    const previous =
      document.activeElement instanceof HTMLElement ? document.activeElement : null
    dialog.showModal()
    return () => {
      dialog.close()
      if (previous?.isConnected) previous.focus()
    }
  }, [])
  return (
    <dialog
      ref={element}
      className="modal"
      aria-labelledby={titleId}
      onCancel={(event) => {
        event.preventDefault()
        if (!busy) onCancel()
      }}
    >
      {children}
    </dialog>
  )
}
