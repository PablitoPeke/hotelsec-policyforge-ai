import type { ApiConnectionState } from '../types/app'

type StatusPillProps = {
  connection: ApiConnectionState
}

export function StatusPill({ connection }: StatusPillProps) {
  const label =
    connection.status === 'online'
      ? `Backend online · ${connection.data.version}`
      : connection.status === 'offline'
        ? 'Backend offline'
        : 'Comprobando backend'

  return (
    <span className={`status-pill status-${connection.status}`}>
      {label}
    </span>
  )
}
