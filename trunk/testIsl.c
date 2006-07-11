/********************************************************************************/
/* Copyright (c) 2004                                                           */
/* Daniel Sleator, David Temperley, and John Lafferty                           */
/* All rights reserved                                                          */
/*                                                                              */
/* Use of the link grammar parsing system is subject to the terms of the        */
/* license set forth in the LICENSE file included with this software,           */ 
/* and also available at http://www.link.cs.cmu.edu/link/license.html           */
/* This license allows free redistribution and use in source and binary         */
/* forms, with or without modification, subject to certain conditions.          */
/*                                                                              */
/********************************************************************************/

#include "link-includes.h"

void test(char *str, Dictionary dict, Parse_Options opts, int should_work) {
  Sentence sent;
  Linkage       linkage;
  char *        diagram;
  int           num_linkages;

  sent = sentence_create(str, dict);
  if (sent == NULL) {
    fprintf(stderr, "%s\n", lperrmsg);
  } else {
    num_linkages = sentence_parse(sent, opts);
    if (should_work && num_linkages == 0)
      fprintf(stderr, "No linkage found for: '%s'\n", str);
    else if (!should_work && num_linkages > 1)
      fprintf(stderr, "Found spurious linkage for: '%s\n'\n", str);
    if (num_linkages > 0) {
      linkage = linkage_create(0, sent, opts);
      printf("%s\n", diagram = linkage_print_diagram(linkage));
      string_delete(diagram);
      linkage_delete(linkage);
    } /*else
        printf("no linkages found for '%s'\n", str);*/
    sentence_delete(sent);
  }
}

int main() {

  Dictionary    dict;
  Parse_Options opts;

  opts  = parse_options_create();
  dict  = dictionary_create("t", NULL, NULL, NULL);

  test("hundur borðar", dict, opts, TRUE);
  test("hundur er vondur", dict, opts, TRUE);
  test("hundurinn er vondi", dict, opts, TRUE);
  test("hundur er vondi", dict, opts, FALSE);

  test("fjölskyldur fá bætur", dict, opts, TRUE);
  test("fjölskyldur fá ekki bætur", dict, opts, TRUE);
  test("fjölskyldur fá bætur í Bretlandi", dict, opts, TRUE);
  test("fjölskyldur fá ekki bætur í Bretlandi", dict, opts, TRUE);
  test("fjölskyldur hryðjuverkamanna fá ekki bætur í Bretlandi", dict, opts, TRUE);
  test("fjölskyldur grunaðra hryðjuverkamanna fá ekki bætur í Bretlandi", dict, opts, TRUE);

  dictionary_delete(dict);
  parse_options_delete(opts);

  return 0;
}
