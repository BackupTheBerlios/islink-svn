(defvar dict-mode-hook nil)

(defvar dict-mode-map
  (let ((dict-mode-map (make-keymap)))
    (define-key dict-mode-map "\C-c\C-c" 'dict-comment-region)
    (define-key dict-mode-map "\C-u\C-c\C-c" 'dict-uncomment-region)
    dict-mode-map)
  "Keymap for DICT major mode")

;(setq auto-mode-alist
;  (append auto-mode-alist
;          (list (cons '"\\.dict$" 'dict-mode))))


(defconst dict-font-lock-keywords-1
  (list
   '("\\<or\\>\\|&" . font-lock-builtin-face)
   '("+" . font-lock-type-face)
   '("-" . font-lock-warning-face))
  "Minimal highlighting expressions for DICT mode")

(defvar dict-font-lock-keywords dict-font-lock-keywords-1
  "Default highlighting expressions for DICT mode")


(defvar dict-mode-syntax-table
  (let ((dict-mode-syntax-table (make-syntax-table)))
    (modify-syntax-entry ?< "$>" dict-mode-syntax-table)
    (modify-syntax-entry ?> "$<" dict-mode-syntax-table)
    (modify-syntax-entry ?% "<" dict-mode-syntax-table)
    (modify-syntax-entry ?\n ">"  dict-mode-syntax-table)
   dict-mode-syntax-table)
  "Syntax table for dict-mode")

(defvar dict-comment-prefix "% "
  "*Comment prefix string for dict-comment and dict-uncomment.  This is
used in regular-expression matching by bst-uncomment, so it should
NOT contain any regular-expression pattern characters like . or *.")

(defun dict-mode ()
  "Major mode for editing Workflow Process Description Language files"
  (interactive)
  (kill-all-local-variables)
  (set-syntax-table dict-mode-syntax-table)
  (use-local-map dict-mode-map)
  (set (make-local-variable 'font-lock-defaults) '(dict-font-lock-keywords))
  (set (make-local-variable 'indent-line-function) 'dict-indent-line)  
  (setq major-mode 'dict-mode)
  (setq mode-name "DICT")

  ;; Syntax information, Syntax table and Font lock support
  (setq comment-end "")
  (setq comment-start "%")
  (setq comment-start-skip "%+ *")

  (run-hooks 'dict-mode-hook))

;;; Local functions
(defun dict-comment-region ()
  "Insert a distinctive comment prefix at the start of each line in
the current region."
  (interactive)
  (let ((start (region-beginning)) (end (region-end)))
    (goto-char start)
    (if (bolp)
        t
      (forward-line 1)
      (setq start (point)))
    (goto-char end)
    (if (bolp)
        t
      (beginning-of-line)
      (setq end (1+ (point))))
    (save-restriction
      (narrow-to-region start end)
      (goto-char start)
      (while (and (bolp) (< (point) (point-max)))
        (insert dict-comment-prefix)
        (forward-line 1)))))


(defun dict-uncomment-region ()
  "Remove a distinctive comment prefix at the start of each line in
the current region."
  (interactive)
  (let ((start (region-beginning)) (end (region-end)) (n (length dict-comment-prefix)))
    (goto-char start)
    (if (bolp)
        t
      (forward-line 1)
      (setq start (point)))
    (goto-char end)
    (if (bolp)
        t
      (beginning-of-line)
      (setq end (1+ (point))))
    (save-restriction
      (narrow-to-region start end)
      (goto-char start)
      (while (and (bolp) (< (point) (point-max)))
        (if (looking-at dict-comment-prefix)
            (delete-char n))
        (forward-line 1)))))

(provide 'dict-mode)

