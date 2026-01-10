/**
 * RTL Utility Functions for Tailwind CSS
 *
 * Provides utility functions to generate RTL-aware class names
 * for margin, padding, and other directional properties.
 */

/**
 * Get margin logical property class for RTL/LTR
 *
 * @param prefix - The margin type (e.g., 'm', 'mx', 'my', 'mt', 'mb', 'ml', 'mr')
 * @param value - The margin value (e.g., '2', '4', 'auto')
 * @param isRTL - Whether the current language is RTL
 * @returns Tailwind CSS class name
 */
export function rtlMargin(prefix: string, value: string | number, isRTL: boolean): string {
  if (prefix === 'm' || prefix === 'p') {
    // All margins/padding
    return `${prefix}-${value}`
  }

  if (prefix === 'mx') {
    // Horizontal margin/padding
    return isRTL ? `ms-${value} me-${value}` : `ms-${value} me-${value}`
  }

  if (prefix === 'my') {
    // Vertical margin/padding
    return `my-${value}`
  }

  if (prefix === 'ml') {
    // Margin/padding left
    return isRTL ? `me-${value}` : `ms-${value}`
  }

  if (prefix === 'mr') {
    // Margin/padding right
    return isRTL ? `ms-${value}` : `me-${value}`
  }

  if (prefix === 'mt') {
    // Margin/padding top
    return `mt-${value}`
  }

  if (prefix === 'mb') {
    // Margin/padding bottom
    return `mb-${value}`
  }

  return `${prefix}-${value}`
}

/**
 * Get border radius logical property class for RTL/LTR
 *
 * @param radius - The border radius value (e.g., '2', '4', 'full')
 * @param isRTL - Whether the current language is RTL
 * @returns Object with individual border radius classes
 */
export function rtlBorderRadius(radius: string | number, isRTL: boolean) {
  return {
    start: isRTL ? `rounded-tr-${radius}` : `rounded-tl-${radius}`,
    end: isRTL ? `rounded-tl-${radius}` : `rounded-tr-${radius}`,
    startStart: isRTL ? `rounded-br-${radius}` : `rounded-bl-${radius}`,
    startEnd: isRTL ? `rounded-bl-${radius}` : `rounded-br-${radius}`,
    endStart: isRTL ? `rounded-tr-${radius}` : `rounded-tl-${radius}`,
    endEnd: isRTL ? `rounded-tl-${radius}` : `rounded-tr-${radius}`,
  }
}

/**
 * Get transform class for RTL icon mirroring
 *
 * @param isRTL - Whether the current language is RTL
 * @returns CSS transform value or empty string
 */
export function rtlMirror(isRTL: boolean): string {
  return isRTL ? 'scale-x-[-1]' : ''
}

/**
 * Get text alignment class for RTL/LTR
 *
 * @param alignment - The desired alignment ('start', 'end', 'center', 'left', 'right')
 * @param isRTL - Whether the current language is RTL
 * @returns Tailwind text alignment class
 */
export function rtlTextAlign(alignment: 'start' | 'end' | 'center' | 'left' | 'right', isRTL: boolean): string {
  if (alignment === 'start') return isRTL ? 'text-right' : 'text-left'
  if (alignment === 'end') return isRTL ? 'text-left' : 'text-right'
  if (alignment === 'center') return 'text-center'
  if (alignment === 'left') return isRTL ? 'text-right' : 'text-left'
  if (alignment === 'right') return isRTL ? 'text-left' : 'text-right'
  return 'text-left'
}

/**
 * Get flex justify content class for RTL/LTR
 *
 * @param justify - The desired justify value ('start', 'end', 'center', 'between', 'around', 'evenly')
 * @param isRTL - Whether the current language is RTL
 * @returns Tailwind justify content class
 */
export function rtlJustify(justify: 'start' | 'end' | 'center' | 'between' | 'around' | 'evenly', isRTL: boolean): string {
  const justifyMap: Record<string, string> = {
    start: isRTL ? 'justify-end' : 'justify-start',
    end: isRTL ? 'justify-start' : 'justify-end',
    center: 'justify-center',
    between: 'justify-between',
    around: 'justify-around',
    evenly: 'justify-evenly',
  }
  return justifyMap[justify] || 'justify-start'
}

/**
 * Get flex align items class for RTL/LTR
 *
 * @param align - The desired align value ('start', 'end', 'center', 'baseline', 'stretch')
 * @param isRTL - Whether the current language is RTL
 * @returns Tailwind align items class
 */
export function rtlAlign(align: 'start' | 'end' | 'center' | 'baseline' | 'stretch', isRTL: boolean): string {
  const alignMap: Record<string, string> = {
    start: 'items-start',
    end: 'items-end',
    center: 'items-center',
    baseline: 'items-baseline',
    stretch: 'items-stretch',
  }
  return alignMap[align] || 'items-start'
}

/**
 * Compose RTL-aware classes for a component
 *
 * @param classes - Object containing ltr and rtl specific classes
 * @param isRTL - Whether the current language is RTL
 * @returns Combined class string
 */
export function rtlClasses(classes: { ltr: string; rtl: string }, isRTL: boolean): string {
  return isRTL ? classes.rtl : classes.ltr
}

/**
 * Get space-x equivalent for RTL
 *
 * @param space - The space value (e.g., '2', '4')
 * @param isRTL - Whether the current language is RTL
 * @returns Tailwind space classes
 */
export function rtlSpaceX(space: string | number, isRTL: boolean): string {
  return isRTL ? `space-x-reverse` : ''
}

/**
 * Get translate transform for RTL animations
 *
 * @param translate - The translate value (e.g., '100%', '-100%', 'full')
 * @param axis - The axis ('x' or 'y')
 * @param isRTL - Whether the current language is RTL
 * @returns Tailwind translate class
 */
export function rtlTranslate(
  translate: string,
  axis: 'x' | 'y',
  isRTL: boolean
): string {
  if (axis === 'y') {
    return `translate-y-${translate}`
  }
  // For X axis, RTL needs to invert the direction
  return isRTL ? `-translate-x-${translate}` : `translate-x-${translate}`
}

/**
 * Generate complete RTL-aware Tailwind classes for common patterns
 *
 * Usage: const classes = rtlPattern({
 *   margin: { ltr: 'ml-4', rtl: 'mr-4' },
 *   padding: { ltr: 'pl-4', rtl: 'pr-4' },
 *   textAlign: { ltr: 'text-left', rtl: 'text-right' },
 * })
 */
export function rtlPattern(patterns: {
  margin?: string
  marginStart?: string
  marginEnd?: string
  padding?: string
  paddingStart?: string
  paddingEnd?: string
  textAlign?: 'start' | 'end' | 'center' | 'left' | 'right'
  justify?: 'start' | 'end' | 'center' | 'between' | 'around' | 'evenly'
  borderRadius?: string
  flexDirection?: 'row' | 'row-reverse'
  mirror?: boolean
}, isRTL: boolean): string {
  const classes: string[] = []

  // Margin
  if (patterns.margin) classes.push(patterns.margin)

  // Margin start (left in LTR, right in RTL)
  if (patterns.marginStart) {
    classes.push(isRTL ? `me-${patterns.marginStart}` : `ms-${patterns.marginStart}`)
  }

  // Margin end (right in LTR, left in RTL)
  if (patterns.marginEnd) {
    classes.push(isRTL ? `ms-${patterns.marginEnd}` : `me-${patterns.marginEnd}`)
  }

  // Padding
  if (patterns.padding) classes.push(patterns.padding)

  // Padding start
  if (patterns.paddingStart) {
    classes.push(isRTL ? `pe-${patterns.paddingStart}` : `ps-${patterns.paddingStart}`)
  }

  // Padding end
  if (patterns.paddingEnd) {
    classes.push(isRTL ? `ps-${patterns.paddingEnd}` : `pe-${patterns.paddingEnd}`)
  }

  // Text align
  if (patterns.textAlign) {
    classes.push(rtlTextAlign(patterns.textAlign, isRTL))
  }

  // Justify content
  if (patterns.justify) {
    classes.push(rtlJustify(patterns.justify, isRTL))
  }

  // Border radius
  if (patterns.borderRadius) {
    const radii = rtlBorderRadius(patterns.borderRadius, isRTL)
    classes.push(radii.start)
  }

  // Flex direction
  if (patterns.flexDirection === 'row') {
    classes.push(isRTL ? 'flex-row-reverse' : 'flex-row')
  } else if (patterns.flexDirection === 'row-reverse') {
    classes.push(isRTL ? 'flex-row' : 'flex-row-reverse')
  }

  // Mirror icon
  if (patterns.mirror) {
    classes.push(rtlMirror(isRTL))
  }

  return classes.join(' ')
}

export default {
  rtlMargin,
  rtlBorderRadius,
  rtlMirror,
  rtlTextAlign,
  rtlJustify,
  rtlAlign,
  rtlClasses,
  rtlSpaceX,
  rtlTranslate,
  rtlPattern,
}
