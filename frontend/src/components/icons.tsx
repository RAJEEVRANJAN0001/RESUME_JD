import React from 'react';

export interface IconProps {
  className?: string;
  size?: number;
}

export const CheckIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 1.06-1.06L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/>
  </svg>
);

export const XMarkIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path d="M4.28 3.22a.75.75 0 0 0-1.06 1.06L6.94 8l-3.72 3.72a.75.75 0 1 0 1.06 1.06L8 9.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L9.06 8l3.72-3.72a.75.75 0 0 0-1.06-1.06L8 6.94 4.28 3.22Z"/>
  </svg>
);

export const WarningIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path fillRule="evenodd" d="M8.893 1.5c-.183-.31-.52-.5-.887-.5s-.703.19-.886.5L.138 13.499a.98.98 0 0 0 0 1.001c.193.31.53.501.886.501h13.964c.367 0 .704-.19.877-.5a1.03 1.03 0 0 0 .01-1.002L8.893 1.5ZM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5Zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2Z" clipRule="evenodd"/>
  </svg>
);

export const RocketIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path d="M14.064 0a8.75 8.75 0 0 0-6.187 2.563l-.459.458c-.314.314-.616.641-.904.979H3.31a1.75 1.75 0 0 0-1.49.833L.11 7.607a.75.75 0 0 0 .418 1.11l3.102.954c.037.051.079.1.124.145l2.429 2.428c.046.046.094.088.145.125l.954 3.102a.75.75 0 0 0 1.11.418l2.774-1.707a1.75 1.75 0 0 0 .833-1.49V9.485c.338-.288.665-.59.979-.904l.458-.459A8.75 8.75 0 0 0 16 1.936V1.75A1.75 1.75 0 0 0 14.25 0h-.186ZM10.5 10.625c-.088.06-.177.118-.266.175l-2.35 1.521.548 1.783 1.949-1.2a.25.25 0 0 0 .119-.213v-2.066ZM3.678 8.116 5.2 5.766c.058-.09.117-.178.176-.266H3.309a.25.25 0 0 0-.213.119l-1.2 1.95 1.782.547ZM12 5a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"/>
  </svg>
);

export const ChartBarIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path d="M1.75 2.5a.75.75 0 0 0-.75.75v9.5c0 .414.336.75.75.75h12.5a.75.75 0 0 0 0-1.5H2.5V3.25a.75.75 0 0 0-.75-.75Z"/>
    <path d="M12.5 6.5a.75.75 0 0 0-.75-.75h-1.5a.75.75 0 0 0-.75.75v4.25h3V6.5ZM8 8.25a.75.75 0 0 0-.75-.75h-1.5a.75.75 0 0 0-.75.75v2.5h3v-2.5ZM4.5 9.75a.75.75 0 0 0-.75-.75h-1.5a.75.75 0 0 0-.75.75v1.25h3V9.75Z"/>
  </svg>
);

export const ClipboardIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path fillRule="evenodd" d="M5.75 1a.75.75 0 0 0-.75.75v3c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-3a.75.75 0 0 0-.75-.75h-4.5Zm.75 3V2.5h3V4h-3Z" clipRule="evenodd"/>
    <path d="M3.5 2.75a.75.75 0 0 0-1.5 0v9.5c0 1.38 1.12 2.5 2.5 2.5h6c1.38 0 2.5-1.12 2.5-2.5v-9.5a.75.75 0 0 0-1.5 0v9.5c0 .55-.45 1-1 1h-6c-.55 0-1-.45-1-1v-9.5Z"/>
  </svg>
);

export const LockIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path fillRule="evenodd" d="M4 4a4 4 0 0 1 8 0v2h.25c.966 0 1.75.784 1.75 1.75v5.5A1.75 1.75 0 0 1 12.25 15h-8.5A1.75 1.75 0 0 1 2 13.25v-5.5C2 6.784 2.784 6 3.75 6H4V4Zm8.5 2V4a2.5 2.5 0 0 0-5 0v2h5Z" clipRule="evenodd"/>
  </svg>
);

export const PaletteIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path d="M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673.848.284.411.537.896.621 1.49a.75.75 0 0 1-1.484.211c-.04-.282-.163-.547-.37-.847a8.456 8.456 0 0 0-.542-.68c-.084-.1-.173-.205-.268-.32C3.201 7.75 2.5 6.766 2.5 5.25 2.5 2.31 4.863 0 8 0s5.5 2.31 5.5 5.25c0 1.516-.701 2.5-1.328 3.259-.095.115-.184.22-.268.319-.207.245-.383.453-.541.681-.208.3-.33.565-.37.847a.751.751 0 0 1-1.485-.212c.084-.593.337-1.078.621-1.489.203-.292.45-.584.673-.848.075-.088.147-.173.213-.253.561-.679.985-1.32.985-2.304 0-2.06-1.637-3.75-4-3.75ZM5.75 10a.75.75 0 0 0-.75.75v1.5a.75.75 0 0 0 1.5 0v-1.5a.75.75 0 0 0-.75-.75Zm4.5 0a.75.75 0 0 0-.75.75v1.5a.75.75 0 0 0 1.5 0v-1.5a.75.75 0 0 0-.75-.75Z"/>
  </svg>
);

export const TargetIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14Zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16Z"/>
    <path d="M8 13A5 5 0 1 1 8 3a5 5 0 0 1 0 10Zm0 1A6 6 0 1 0 8 2a6 6 0 0 0 0 12Z"/>
    <path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6Zm0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z"/>
    <path d="M9.5 8a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Z"/>
  </svg>
);

export const DocumentTextIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path fillRule="evenodd" d="M4 1.75C4 .784 4.784 0 5.75 0h5.586c.464 0 .909.184 1.237.513l2.914 2.914c.329.328.513.773.513 1.237v9.586A1.75 1.75 0 0 1 14.25 16h-8.5A1.75 1.75 0 0 1 4 14.25V1.75Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25V6h-2.75A1.75 1.75 0 0 1 10 4.25V1.5H5.75Z" clipRule="evenodd"/>
    <path d="M11.5 1.75v2.5c0 .138.112.25.25.25h2.5L11.5 1.75Z"/>
  </svg>
);

export const CubeIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path d="M7.752.066a.5.5 0 0 1 .496 0l6.75 4a.5.5 0 0 1 0 .868l-6.75 4a.5.5 0 0 1-.496 0l-6.75-4a.5.5 0 0 1 0-.868l6.75-4ZM1.456 4.5L8 7.88l6.544-3.38L8 1.12 1.456 4.5Z"/>
    <path d="M.5 5.934v5a.5.5 0 0 0 .248.434l6.75 4a.5.5 0 0 0 .504 0l6.75-4a.5.5 0 0 0 .248-.434v-5L8 9.88.5 5.934Z"/>
  </svg>
);

export const SparklesIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path d="M8.5 2.687c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-2.213.492V2.687zM8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 2.629.537l.013.256c.020.414.36.45.572.1C7.78 13.57 8 13.25 8 12.5V1.783z"/>
  </svg>
);

export const WrenchIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path d="M.102 2.223A3.004 3.004 0 0 0 3.78 5.897l6.341 6.252a3.003 3.003 0 0 0 4.238-4.237L8.017 1.68a3.004 3.004 0 0 0-7.915.543ZM2.494 1.92a2.003 2.003 0 0 1 4.237-.006l1.086 1.086a.5.5 0 0 0 .708 0l.708-.708a.5.5 0 0 1 .708.708l-.708.708a.5.5 0 0 0 0 .708l1.086 1.086a2.003 2.003 0 0 1-.006 4.237l-6.252-6.341a2.003 2.003 0 0 1 .543-1.48Z"/>
  </svg>
);

export const CircleStackIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path d="M1.75 10.5a.75.75 0 0 1 .75-.75h11a.75.75 0 0 1 0 1.5h-11a.75.75 0 0 1-.75-.75ZM1.75 6.75a.75.75 0 0 1 .75-.75h11a.75.75 0 0 1 0 1.5h-11a.75.75 0 0 1-.75-.75ZM1.75 3a.75.75 0 0 1 .75-.75h11a.75.75 0 0 1 0 1.5h-11A.75.75 0 0 1 1.75 3Z"/>
  </svg>
);

export const DevicePhoneMobileIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path d="M4.5 2A1.5 1.5 0 0 0 3 3.5v9A1.5 1.5 0 0 0 4.5 14h7a1.5 1.5 0 0 0 1.5-1.5v-9A1.5 1.5 0 0 0 11.5 2h-7ZM4.5 3.5h7v9h-7v-9Z"/>
    <path d="M8 11.5a.5.5 0 1 0 0 1 .5.5 0 0 0 0-1Z"/>
  </svg>
);

export const WrenchScrewdriverIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path fillRule="evenodd" d="M14.12 1.88a.5.5 0 0 1 0 .708l-2.83 2.829a.5.5 0 0 1-.708 0L8.288 3.121a.5.5 0 0 1 0-.708l2.83-2.829a.5.5 0 0 1 .708 0L14.12 1.88ZM6.95 6.243 2.415 10.78a1.5 1.5 0 0 0 2.122 2.122L9.07 8.365l-.707-.707-1.414 1.414a.5.5 0 1 1-.708-.708l1.414-1.414-.707-.707Z" clipRule="evenodd"/>
    <path d="M1.061 9.719A1.003 1.003 0 0 0 2.48 11.14l2.829-2.83a1.003 1.003 0 0 0-1.419-1.42L1.061 9.719Z"/>
  </svg>
);

export const TrophyIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path d="M2.5 8.5A2.5 2.5 0 0 1 0 6v-.5C0 4.01 1.01 3 2.25 3H4v2.25A2.75 2.75 0 0 0 6.75 8H7.5v1.5h-1a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5h-1V8h.75A2.75 2.75 0 0 0 12 5.25V3h1.75C14.99 3 16 4.01 16 5.25V6a2.5 2.5 0 0 1-2.5 2.5H12v-.25A1.25 1.25 0 0 1 10.75 7h-5.5A1.25 1.25 0 0 1 4 8.25V8.5h-1.5Z"/>
  </svg>
);

export const HeartIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path d="M8 14.5s-6-5.5-6-9.5a4.5 4.5 0 0 1 9 0c0 .5-.1 1-.3 1.5a.75.75 0 0 0 1.4.5c.3-.7.4-1.3.4-2A6 6 0 0 0 2 5c0 5.2 6 10.5 6 10.5s6-5.3 6-10.5A6 6 0 0 0 8 14.5Z"/>
  </svg>
);

export const InformationCircleIcon: React.FC<IconProps> = ({ className = "", size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 16 16" fill="currentColor" className={className}>
    <path fillRule="evenodd" d="M15 8A7 7 0 1 1 1 8a7 7 0 0 1 14 0ZM9 5a1 1 0 1 1-2 0 1 1 0 0 1 2 0ZM6.75 8a.75.75 0 0 0 0 1.5h.75v1.75a.75.75 0 0 0 1.5 0V9.5h.25a.75.75 0 0 0 0-1.5h-2.5Z" clipRule="evenodd"/>
  </svg>
);